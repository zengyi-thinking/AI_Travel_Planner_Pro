"""
User Service

This module provides business logic for user operations.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import create_access_token
from app.modules.users.models.user import User
from app.modules.users.daos.user_dao import UserDAO


class UserService:
    """
    User business logic service
    """
    
    def __init__(self, db: Session):
        """
        Initialize UserService
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_dao = UserDAO(db)
    
    def register_user(
        self,
        email: str,
        password: str,
        name: str
    ) -> tuple[User, str]:
        """
        Register a new user
        
        Args:
            email: User email
            password: User password
            name: User name
            
        Returns:
            Tuple of (user, access_token)
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        if self.user_dao.email_exists(email):
            raise ValueError("Email already registered")
        
        # Create user
        hashed_pwd = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_pwd,
            name=name,
            is_active=True,
            membership_level='free'
        )
        
        user = self.user_dao.create(user)
        
        # Create access token
        access_token = create_access_token(subject=str(user.id))
        
        return user, access_token
    
    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[tuple[User, str]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (user, access_token) or None if authentication fails
        """
        # Get user by email
        user = self.user_dao.get_by_email(email)
        
        if not user:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
        # Create access token
        access_token = create_access_token(subject=str(user.id))
        
        return user, access_token
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        return self.user_dao.get_by_id(user_id)
    
    def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[User]:
        """
        Update user
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object or None
        """
        # Remove sensitive fields from kwargs
        sensitive_fields = ['id', 'hashed_password', 'email', 'created_at']
        for field in sensitive_fields:
            kwargs.pop(field, None)
        
        return self.user_dao.update(user_id, **kwargs)
    
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed, False otherwise
            
        Raises:
            ValueError: If old password is incorrect
        """
        user = self.user_dao.get_by_id(user_id)
        
        if not user:
            return False
        
        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            raise ValueError("Incorrect password")
        
        # Update password
        hashed_new_pwd = hash_password(new_password)
        self.user_dao.update(user_id, hashed_password=hashed_new_pwd)
        
        return True
