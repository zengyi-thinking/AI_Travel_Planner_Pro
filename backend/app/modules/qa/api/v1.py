"""
QA Module API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.common.dtos.base import ResponseDTO, PaginationDTO
from app.modules.qa.schemas.chat_schema import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from app.modules.qa.services.chat_service import ChatService

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
    service = ChatService(db)
    return ResponseDTO(data=service.mock_weather(city))


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
