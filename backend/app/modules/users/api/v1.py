"""
Users API Routes (v1)

This module contains all authentication and user management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user, get_current_active_user
from app.core.security.jwt import create_access_token
from app.modules.users.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin
)
from app.modules.users.schemas.auth import TokenResponse
from app.modules.users.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    """
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access token.
    """
    user_service = UserService(db)
    user = await user_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    """
    Get current user information.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update current user information.
    """
    user_service = UserService(db)
    updated_user = await user_service.update_user(current_user.id, user_data)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete current user account.
    """
    user_service = UserService(db)
    await user_service.delete_user(current_user.id)
