"""
Base DTO Classes

This module contains base DTO (Data Transfer Object) classes used across the application.
DTOs are used for request/response serialization and validation.
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List
from datetime import datetime


T = TypeVar('T')


class BaseDTO(BaseModel):
    """
    Base DTO with common configuration.
    """
    class Config:
        from_attributes = True
        use_enum_values = True


class ResponseDTO(BaseDTO):
    """
    Standard API response DTO.
    """
    success: bool = True
    code: int = 200
    message: str = "Success"
    data: Optional[dict] = None


class ErrorResponseDTO(BaseDTO):
    """
    Standard error response DTO.
    """
    success: bool = False
    code: int = 400
    message: str = "Error"
    error: Optional[str] = None


class PaginationDTO(BaseDTO):
    """
    Pagination metadata DTO.
    """
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, le=100, description="Items per page")
    total: int = Field(..., ge=0, description="Total items count")
    pages: int = Field(..., ge=0, description="Total pages count")


class PaginatedResponseDTO(BaseDTO):
    """
    Standard paginated response DTO.
    """
    items: List[dict]
    pagination: PaginationDTO


class ListRequestDTO(BaseDTO):
    """
    Standard list request DTO with pagination.
    """
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Items per page")
    search: Optional[str] = Field(None, description="Search query")


class TimestampDTO(BaseModel):
    """
    DTO with timestamp fields.
    """
    created_at: datetime
    updated_at: datetime
