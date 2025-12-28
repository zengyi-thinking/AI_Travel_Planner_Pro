"""
QA Module API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.common.dtos.base import ResponseDTO, PaginationDTO
from app.modules.qa.schemas.chat_schema import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from app.modules.qa.services.chat_service import ChatService
from app.modules.qa.tools.weather import query_weather as query_weather_tool
from app.core.config import settings
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sessions", response_model=ResponseDTO)
async def create_chat_session(
    chat_data: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    session = await service.create_session(current_user.id, chat_data)
    features = service.parse_features(session.features_json)
    session_payload = ChatResponse(
        id=session.id,
        title=session.title,
        features=features,
        created_at=session.created_at
    )
    return ResponseDTO(data={"session": session_payload.model_dump()})


@router.get("/sessions", response_model=ResponseDTO)
async def list_chat_sessions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    service = ChatService(db)
    sessions = await service.list_sessions(current_user.id, page=page, size=size)
    total = await service.count_sessions(current_user.id)
    pages = (total + size - 1) // size if size else 0
    items = [
        ChatResponse(
            id=session.id,
            title=session.title,
            features=service.parse_features(session.features_json),
            created_at=session.created_at
        ).model_dump()
        for session in sessions
    ]
    pagination = PaginationDTO(page=page, size=size, total=total, pages=pages).model_dump()
    return ResponseDTO(data={"items": items, "pagination": pagination})


@router.post("/messages/stream")
async def send_message_stream(
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """流式发送消息"""
    service = ChatService(db)

    try:
        # 验证会话
        session = await service.get_session(current_user.id, message_data.session_id)
        if not session:
            raise ValueError("Session not found")

        # 获取历史消息
        history_messages = await service.message_dao.list_by_conversation(
            conversation_id=session.id,
            offset=0,
            limit=10
        )
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]

        # 保存用户消息
        user_message = await service.message_dao.create(
            service._user_message_constructor(message_data.content, message_data.message_type, session.id)
        )

        features = service.parse_features(session.features_json)
        use_rag = features.knowledge_base if features else True
        agent = service._get_agent(use_rag=use_rag)

        async def generate_stream():
            """生成流式响应"""
            try:
                # 使用agent生成流式响应
                async for chunk in agent.chat_stream(message_data.content, history, use_rag=use_rag):
                    # 发送SSE格式的数据
                    yield f"data: {json.dumps({'chunk': chunk}, ensure_ascii=False)}\n\n"

                # 流式结束
                yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"

                # 保存完整的AI回复到数据库
                full_response = ""
                async for chunk in agent.chat_stream(message_data.content, history, use_rag=use_rag):
                    full_response += chunk

                assistant_message = await service.message_dao.create(
                    service._assistant_message_constructor(full_response, session.id)
                )

                # 发送最终消息ID
                yield f"data: {json.dumps({'message_id': assistant_message.id}, ensure_ascii=False)}\n\n"

            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/messages", response_model=ResponseDTO)
async def send_message(
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """非流式发送消息（备用接口）"""
    service = ChatService(db)
    try:
        timeout_seconds = settings.AI_TIMEOUT or 60
        message = await asyncio.wait_for(
            service.send_message(current_user.id, message_data),
            timeout=timeout_seconds
        )
    except asyncio.TimeoutError:
        logger.error("QA message timeout after %ss", timeout_seconds)
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="QA response timeout")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    message_payload = MessageResponse(
        id=message.id,
        session_id=message.conversation_id,
        role=message.role,
        content=message.content,
        message_type=message.message_type,
        created_at=message.created_at
    )
    return ResponseDTO(data={"message": message_payload.model_dump()})


@router.get("/sessions/{session_id}/messages", response_model=ResponseDTO)
async def get_chat_history(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200)
):
    service = ChatService(db)
    messages = await service.list_messages(current_user.id, session_id, page=page, size=size)
    total = await service.count_messages(current_user.id, session_id)
    pages = (total + size - 1) // size if size else 0
    items = [
        MessageResponse(
            id=msg.id,
            session_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            message_type=msg.message_type,
            created_at=msg.created_at
        ).model_dump()
        for msg in messages
    ]
    pagination = PaginationDTO(page=page, size=size, total=total, pages=pages).model_dump()
    return ResponseDTO(data={"items": items, "pagination": pagination})


@router.post("/messages", response_model=ResponseDTO)
async def send_message(
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    try:
        message = await service.send_message(current_user.id, message_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    message_payload = MessageResponse(
        id=message.id,
        session_id=message.conversation_id,
        role=message.role,
        content=message.content,
        message_type=message.message_type,
        created_at=message.created_at
    )
    return ResponseDTO(data={"message": message_payload.model_dump()})


@router.get("/sessions/{session_id}/messages", response_model=ResponseDTO)
async def get_chat_history(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200)
):
    service = ChatService(db)
    messages = await service.list_messages(current_user.id, session_id, page=page, size=size)
    total = await service.count_messages(current_user.id, session_id)
    pages = (total + size - 1) // size if size else 0
    items = [
        MessageResponse(
            id=msg.id,
            session_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            message_type=msg.message_type,
            created_at=msg.created_at
        ).model_dump()
        for msg in messages
    ]
    pagination = PaginationDTO(page=page, size=size, total=total, pages=pages).model_dump()
    return ResponseDTO(data={"items": items, "pagination": pagination})


@router.get("/weather/{city}", response_model=ResponseDTO)
async def query_weather(
    city: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        return ResponseDTO(data=await query_weather_tool(city))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))


@router.post("/speech-to-text", response_model=ResponseDTO)
async def speech_to_text(
    audio: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    return ResponseDTO(data=service.mock_speech_to_text())


@router.post("/text-to-speech", response_model=ResponseDTO)
async def text_to_speech(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    text = payload.get("text", "")
    return ResponseDTO(data=service.mock_text_to_speech(text))
