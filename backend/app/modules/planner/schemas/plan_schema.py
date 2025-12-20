"""
Plan Schemas

This module contains Pydantic models for travel plan data.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PlanBase(BaseModel):
    """
    Base plan schema.
    """
    title: str = Field(..., min_length=1, max_length=200)
    destination: str = Field(..., min_length=1, max_length=200)
    departure: Optional[str] = Field(None, max_length=200)
    days: int = Field(..., ge=1, le=365)
    budget: Optional[float] = Field(None, ge=0)
    travel_style: str = Field("leisure", regex="^(leisure|adventure|foodie)$")


class PlanCreate(PlanBase):
    """
    Schema for plan creation.
    """
    pass


class PlanUpdate(BaseModel):
    """
    Schema for plan updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    budget: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, regex="^(draft|active|completed|archived)$")


class DayDetail(BaseModel):
    """
    Schema for daily itinerary detail.
    """
    day_number: int
    date: Optional[datetime]
    title: Optional[str]
    activities: List[dict] = []


class PlanResponse(PlanBase):
    """
    Schema for plan response.
    """
    id: int
    user_id: int
    status: str
    ai_generated: bool
    days_detail: List[DayDetail] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
