"""
JWT Token Utilities

This module provides JWT token creation and verification functionality.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from app.core.config import settings


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        subject: User ID or identifier
        expires_delta: Custom expiration time
        
    Returns:
        Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode: Dict[str, Any] = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token to verify
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from JWT token
    
    Args:
        token: JWT token
        
    Returns:
        User ID or None if invalid
    """
    payload = verify_token(token)
    if payload and "sub" in payload:
        try:
            return int(payload["sub"])
        except ValueError:
            return None
    return None
