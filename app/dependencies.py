from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.core.security import decode_access_token
from app.core.exceptions import AuthenticationException, UserNotFoundException
from app.services.auth_service import AuthService


# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        AuthenticationException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise AuthenticationException("Invalid token")
    
    # Get user ID from token
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise AuthenticationException("Invalid token payload")
    
    # Get user from database
    try:
        user = await AuthService.get_user_by_id(db, int(user_id))
    except ValueError:
        raise AuthenticationException("Invalid user ID in token")
    
    if user is None:
        raise UserNotFoundException()
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to ensure current user is active.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
        
    Raises:
        AuthenticationException: If user is inactive
    """
    if not current_user.is_active:
        raise AuthenticationException("User account is inactive")
    
    return current_user