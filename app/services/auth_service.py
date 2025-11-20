from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import Optional

from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InactiveUserException,
    UserNotFoundException,
)


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            UserAlreadyExistsException: If user with email already exists
        """
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise UserAlreadyExistsException()
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        now = datetime.now(timezone.utc)
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            phone=user_data.phone,
            company_name=user_data.company_name,
            is_active=True,
            is_deleted=False,
            created_at=now,
            updated_at=now,
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> User:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            login_data: User login credentials
            
        Returns:
            Authenticated user object
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
            InactiveUserException: If user account is inactive
        """
        # Get user by email
        result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user or user.is_deleted:
            raise InvalidCredentialsException()
        
        # Verify password
        if not verify_password(login_data.password, user.password):
            raise InvalidCredentialsException()
        
        # Check if user is active
        if not user.is_active:
            raise InactiveUserException()
        
        return user
    
    @staticmethod
    def create_user_token(user: User) -> str:
        """
        Create JWT access token for user.
        
        Args:
            user: User object
            
        Returns:
            JWT access token string
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
        }
        
        return create_access_token(token_data)
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object or None
        """
        result = await db.execute(
            select(User).where(
                User.id == user_id,
                User.is_deleted == False,
                User.is_active == True
            )
        )
        return result.scalar_one_or_none()