"""
Base Exceptions

This module defines the base exception classes used throughout the application.
All custom exceptions should inherit from these base classes.
"""

from fastapi import HTTPException, status


class WanderFlowException(Exception):
    """
    Base exception for all WanderFlow application errors.
    """
    def __init__(self, message: str, code: int = None):
        self.message = message
        self.code = code or 500
        super().__init__(self.message)


class ValidationException(WanderFlowException):
    """
    Exception raised when data validation fails.
    """
    def __init__(self, message: str):
        super().__init__(message, 422)


class NotFoundException(WanderFlowException):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class UnauthorizedException(WanderFlowException):
    """
    Exception raised when user is not authorized to access a resource.
    """
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class ForbiddenException(WanderFlowException):
    """
    Exception raised when user is forbidden to access a resource.
    """
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)


class ConflictException(WanderFlowException):
    """
    Exception raised when there's a conflict with current state.
    """
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)


class ServiceUnavailableException(WanderFlowException):
    """
    Exception raised when an external service is unavailable.
    """
    def __init__(self, message: str = "Service unavailable"):
        super().__init__(message, 503)


def http_exception_from_wanderflow_exception(exc: WanderFlowException) -> HTTPException:
    """
    Convert WanderFlowException to FastAPI HTTPException.

    Args:
        exc: WanderFlow exception

    Returns:
        FastAPI HTTPException
    """
    return HTTPException(
        status_code=exc.code,
        detail={
            "success": False,
            "code": exc.code,
            "message": exc.message,
            "error": exc.__class__.__name__
        }
    )
