"""
Itinerary Model

This module defines the SQLAlchemy model for itineraries.
"""

from sqlalchemy import Column, String, Integer, Numeric, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.core.db.base import BaseModel


class Itinerary(BaseModel):
    """
    Itinerary database model.
    """
    __tablename__ = "itineraries"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False, index=True)
    departure = Column(String(200), nullable=True)
    days = Column(Integer, nullable=False)
    budget = Column(Numeric(12, 2), nullable=True)
    travel_style = Column(String(20), default="leisure", nullable=False)
    status = Column(String(20), default="draft", nullable=False)
    ai_generated = Column(SqlEnum("draft", "active", "completed", "archived"), default="draft")
    metadata = Column(Text, nullable=True)  # JSON field

    # Relationships
    days_detail = relationship("DayDetail", back_populates="itinerary", cascade="all, delete-orphan")


class DayDetail(BaseModel):
    """
    Day detail database model.
    """
    __tablename__ = "itinerary_days"

    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    date = Column(String(10), nullable=True)  # YYYY-MM-DD format
    title = Column(String(200), nullable=True)
    activities = Column(Text, nullable=True)  # JSON field
    notes = Column(Text, nullable=True)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="days_detail")
