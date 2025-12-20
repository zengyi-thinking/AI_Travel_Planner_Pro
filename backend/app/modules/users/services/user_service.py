"""
User Service

This module contains business logic for user operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.daos.user_dao import UserDAO
from app.modules.users.schemas.user import UserCreate, UserUpdate, UserResponse
from app.common.exceptions.base import NotFoundException
from typing import Optional

import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for user business logic.
    """

    def __init__(self, db_session: AsyncSession):
        self.user_dao = UserDAO(db_session)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user response
        """
        user = await self.user_dao.create_user(user_data.dict())
        return UserResponse.from_orm(user)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User response

        Raises:
            NotFoundException: If user not found
        """
        user = await self.user_dao.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.from_orm(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """
        Update user information.

        Args:
            user_id: User ID
            user_data: Updated user data

        Returns:
            Updated user response
        """
        user = await self.user_dao.update_user(user_id, user_data.dict(exclude_unset=True))
        return UserResponse.from_orm(user)

    async def delete_user(self, user_id: int) -> None:
        """
        Delete user.

        Args:
            user_id: User ID
        """
        await self.user_dao.delete_user(user_id)

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """
        Authenticate user.

        Args:
            email: User email
            password: Plain password

        Returns:
            User response if authenticated, None otherwise
        """
        user = await self.user_dao.authenticate_user(email, password)
        if user:
            return UserResponse.from_orm(user)
        return None
