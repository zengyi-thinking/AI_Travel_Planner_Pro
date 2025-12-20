"""
User Data Access Object (DAO)

This module handles all database operations for users.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.modules.users.models.user import User
from app.core.security.jwt import get_password_hash, verify_password
from app.common.exceptions.base import NotFoundException, ConflictException
import logging

logger = logging.getLogger(__name__)


class UserDAO:
    """
    Data Access Object for user operations.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User object or None
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: dict) -> User:
        """
        Create a new user.

        Args:
            user_data: User data dictionary

        Returns:
            Created user object

        Raises:
            ConflictException: If email already exists
        """
        # Hash password
        user_data["password_hash"] = get_password_hash(user_data["password"])
        del user_data["password"]

        # Create user
        user = User(**user_data)
        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise ConflictException("Email already exists")

    async def update_user(self, user_id: int, user_data: dict) -> User:
        """
        Update user information.

        Args:
            user_id: User ID
            user_data: Updated user data

        Returns:
            Updated user object

        Raises:
            NotFoundException: If user not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        # Update fields
        for key, value in user_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        """
        Delete user.

        Args:
            user_id: User ID

        Raises:
            NotFoundException: If user not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        await self.db.delete(user)
        await self.db.commit()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: Plain password

        Returns:
            User object if authenticated, None otherwise
        """
        user = await self.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
