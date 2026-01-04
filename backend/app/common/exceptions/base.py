"""
Base Exceptions

This module defines the base exception classes used throughout the application.
All custom exceptions should inherit from these base classes.
"""

from fastapi import HTTPException, status
from typing import Optional, Any, Dict


class WanderFlowException(Exception):
    """
    Base exception for all WanderFlow application errors.
    """
    def __init__(self, message: str, code: int = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code or 500
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(WanderFlowException):
    """
    Exception raised when data validation fails.
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, details)


class NotFoundException(WanderFlowException):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, details)


class UnauthorizedException(WanderFlowException):
    """
    Exception raised when user is not authorized to access a resource.
    """
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 401, details)


class ForbiddenException(WanderFlowException):
    """
    Exception raised when user is forbidden to access a resource.
    """
    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, details)


class ConflictException(WanderFlowException):
    """
    Exception raised when there's a conflict with current state.
    """
    def __init__(self, message: str = "Conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 409, details)


class ServiceUnavailableException(WanderFlowException):
    """
    Exception raised when an external service is unavailable.
    """
    def __init__(self, message: str = "Service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 503, details)


class QuotaExceededException(WanderFlowException):
    """
    Exception raised when user exceeds their usage quota.

    Attributes:
        message: Human-readable error message
        usage: Current usage count
        limit: Usage limit
        upgrade_url: URL to upgrade page (optional)
        quota_type: Type of quota ('plan', 'copywriter', etc.)
    """
    def __init__(
        self,
        message: str,
        usage: int,
        limit: int,
        quota_type: str = "usage",
        upgrade_url: str = "/settings?tab=subscription"
    ):
        details = {
            "usage": usage,
            "limit": limit,
            "quota_type": quota_type,
            "upgrade_url": upgrade_url,
            "unlimited": limit == -1
        }
        super().__init__(message, 403, details)


def http_exception_from_wanderflow_exception(exc: WanderFlowException) -> HTTPException:
    """
    Convert WanderFlowException to FastAPI HTTPException.

    Args:
        exc: WanderFlow exception

    Returns:
        FastAPI HTTPException with unified error format
    """
    error_response = {
        "success": False,
        "code": exc.code,
        "message": exc.message,
        "error": exc.__class__.__name__
    }

    # Include details if present
    if exc.details:
        error_response["details"] = exc.details

    return HTTPException(
        status_code=exc.code,
        detail=error_response
    )
