"""
User Schemas

This module contains Pydantic models for user-related data validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base user schema with common fields.
    """
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """
    Schema for user creation.
    """
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    """
    Schema for user updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Schema for user response (without sensitive data).
    """
    id: int
    status: str
    email_verified: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
