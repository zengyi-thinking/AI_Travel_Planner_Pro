"""
User Model

This module defines the User database model using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.core.db.base import Base


class User(Base):
    """
    User model
    
    Attributes:
        id: Primary key
        email: User email (unique)
        hashed_password: Hashed password
        name: User full name
        is_active: Whether the user account is active
        membership_level: User membership level (free/pro)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Required fields
    email = Column(String(255), unique=True, index=True, nullable=False, comment="User email")
    hashed_password = Column(String(255), nullable=False, comment="Hashed password")
    name = Column(String(100), nullable=False, comment="User full name")
    
    # Optional fields
    is_active = Column(Boolean, default=True, nullable=False, comment="Account status")
    membership_level = Column(
        Enum('free', 'pro', name='membership_levels'),
        default='free',
        nullable=False,
        comment="Membership level"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Account creation time"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update time"
    )
    
    # Relationships
    # Example: itineraries = relationship("Itinerary", back_populates="user")
