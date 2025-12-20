"""
User API Routes

This module defines FastAPI routes for user operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.users.services.user_service import UserService
from app.modules.users.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    LoginResponse,
    RegisterResponse,
    PasswordChange
)
from app.modules.users.models.user import User
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        user_service = UserService(db)
        user, access_token = user_service.register_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        
        return RegisterResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token
    """
    user_service = UserService(db)
    result = user_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user, access_token = result
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user information
    """
    user_service = UserService(db)
    updated_user = user_service.update_user(
        user_id=current_user.id,
        name=user_data.name
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(updated_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change user password
    """
    user_service = UserService(db)
    
    try:
        user_service.change_password(
            user_id=current_user.id,
            old_password=password_data.old_password,
            new_password=password_data.new_password
        )
        
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
