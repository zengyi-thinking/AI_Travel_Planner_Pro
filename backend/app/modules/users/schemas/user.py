"""
User Schemas

This module defines Pydantic models for user API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Base user schema
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    membership_level: str = Field(default='free')


# User creation schema
class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=128)


# User login schema
class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


# User update schema
class UserUpdate(BaseModel):
    """Schema for user update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)


# User response schema
class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Token response schema
class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Login response schema
class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Register response schema
class RegisterResponse(BaseModel):
    """Schema for register response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Password change schema
class PasswordChange(BaseModel):
    """Schema for password change"""
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=128)
