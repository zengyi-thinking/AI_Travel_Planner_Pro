"""
User Model

This module defines the SQLAlchemy model for user data.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text
from app.core.db.base import BaseModel


class User(BaseModel):
    """
    User database model.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
