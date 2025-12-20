"""
User Data Access Object (DAO)

This module provides database access operations for users.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.modules.users.models.user import User


class UserDAO:
    """
    Data Access Object for User model
    """
    
    def __init__(self, db: Session):
        """
        Initialize UserDAO
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_by_id(self, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> User:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User object or None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: User) -> User:
        """
        Create a new user
        
        Args:
            user: User object
            
        Returns:
            Created user object
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, **kwargs) -> User:
        """
        Update user
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object
        """
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email exists
        
        Args:
            email: Email to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(User).filter(User.email == email).first() is not None
