"""
QA Chat Service
"""

import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.qa.daos.conversation_dao import ConversationDAO
from app.modules.qa.daos.message_dao import MessageDAO
from app.modules.qa.models.conversation import Conversation
from app.modules.qa.models.message import Message
from app.modules.qa.schemas.chat_schema import ChatCreate, ChatFeatures, MessageCreate
from app.modules.qa.rag.knowledge_base import get_knowledge_base


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversation_dao = ConversationDAO(db)
        self.message_dao = MessageDAO(db)

    async def create_session(self, user_id: int, data: ChatCreate) -> Conversation:
        features_json = None
        if data.features:
            features_json = data.features.model_dump_json()

        conversation = Conversation(
            user_id=user_id,
            title=data.title or "新对话",
            features_json=features_json
        )
        return await self.conversation_dao.create(conversation)

    async def list_sessions(
        self,
        user_id: int,
        page: int = 1,
        size: int = 20
    ) -> List[Conversation]:
        offset = max(page - 1, 0) * size
        return await self.conversation_dao.list_by_user(
            user_id=user_id,
            offset=offset,
            limit=size
        )

    async def count_sessions(self, user_id: int) -> int:
        return await self.conversation_dao.count_by_user(user_id)

    async def get_session(self, user_id: int, session_id: int) -> Optional[Conversation]:
        return await self.conversation_dao.get_by_id(session_id, user_id)

    async def list_messages(
        self,
        user_id: int,
        session_id: int,
        page: int = 1,
        size: int = 50
    ) -> List[Message]:
        session = await self.get_session(user_id, session_id)
        if not session:
            return []
        offset = max(page - 1, 0) * size
        return await self.message_dao.list_by_conversation(
            conversation_id=session_id,
            offset=offset,
            limit=size
        )

    async def count_messages(self, user_id: int, session_id: int) -> int:
        session = await self.get_session(user_id, session_id)
        if not session:
            return 0
        return await self.message_dao.count_by_conversation(session_id)

    async def send_message(self, user_id: int, data: MessageCreate) -> Message:
        session = await self.get_session(user_id, data.session_id)
        if not session:
            raise ValueError("Session not found")

        user_message = Message(
            conversation_id=session.id,
            role="user",
            content=data.content,
            message_type=data.message_type
        )
        await self.message_dao.create(user_message)

        assistant_content = await self._build_response(session.features_json, data.content)
        assistant_message = Message(
            conversation_id=session.id,
            role="assistant",
            content=assistant_content,
            message_type="text"
        )
        return await self.message_dao.create(assistant_message)

    async def _build_response(self, features_json: Optional[str], content: str) -> str:
        features = self.parse_features(features_json)
        knowledge_base = get_knowledge_base()
        if features and features.knowledge_base:
            return await knowledge_base.generate_answer(content)

        response = await knowledge_base.generate_general_answer(content)
        return response or (
            f"我理解您的问题是：\"{content}\"。\n\n"
            "我可以提供：\n"
            "1) 行程规划建议\n"
            "2) 天气与出行提示\n"
            "3) 签证与政策说明\n"
            "4) 美食与景点推荐\n"
        )

    def parse_features(self, features_json: Optional[str]) -> Optional[ChatFeatures]:
        if not features_json:
            return None
        return ChatFeatures.model_validate_json(features_json)

    def mock_weather(self, city: str) -> dict:
        today = datetime.utcnow().date()
        forecast = []
        for index in range(3):
            forecast.append({
                "date": str(today),
                "weather": ["晴", "多云", "小雨"][index % 3],
                "temp_high": 26 + index,
                "temp_low": 18 + index,
                "humidity": 60 + index * 3,
                "wind": "南风3级",
                "uv_index": 5 + index
            })
        return {"city": city, "forecast": forecast}

    def mock_speech_to_text(self) -> dict:
        return {"text": "帮我查询一下北京的天气"}

    def mock_text_to_speech(self, text: str) -> dict:
        return {"audio_url": "https://example.com/audio/mock.mp3", "duration": 3.5}
