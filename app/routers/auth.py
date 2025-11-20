from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    AuthResponse,
    UserResponse,
    TokenResponse,
    MessageResponse,
)
from app.models.user import User
from app.services.auth_service import AuthService
from app.dependencies import get_current_active_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and return user data with access token",
)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.
    
    - **name**: User's full name (min 2 characters)
    - **email**: Valid email address (must be unique)
    - **password**: Password (min 8 characters)
    - **phone**: Optional phone number
    - **company_name**: Optional company name
    """
    # Create user
    user = await AuthService.register_user(db, user_data)
    
    # Create access token
    access_token = AuthService.create_user_token(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=TokenResponse(access_token=access_token, token_type="bearer"),
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and return user data with access token",
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    """
    # Authenticate user
    user = await AuthService.authenticate_user(db, login_data)
    
    # Create access token
    access_token = AuthService.create_user_token(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=TokenResponse(access_token=access_token, token_type="bearer"),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get current authenticated user information",
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current authenticated user data.
    
    Requires valid Bearer token in Authorization header.
    """
    return UserResponse.model_validate(current_user)


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logout current user (token should be discarded on client side)",
)
async def logout(
    current_user: User = Depends(get_current_active_user),
):
    """
    Logout current user.
    
    Note: JWT tokens are stateless. Client should discard the token.
    For production, implement token blacklisting if needed.
    """
    return MessageResponse(message="Successfully logged out")


@router.post(
    "/debug/login",
    status_code=status.HTTP_200_OK,
    summary="Debug Login (Development Only)",
    description="Debug endpoint to check password hashing - REMOVE IN PRODUCTION!",
    include_in_schema=True,
)
async def debug_login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    ⚠️ DEVELOPMENT ONLY - REMOVE IN PRODUCTION!
    
    Shows password comparison details for debugging.
    """
    from app.config import settings
    
    # Block in production
    if not settings.DEBUG:
        return {"error": "This endpoint is disabled in production"}
    
    from app.core.security import verify_password, get_password_hash
    from sqlalchemy import select
    
    # Get user by email
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return {
            "error": "User not found",
            "email": login_data.email,
            "user_exists": False
        }
    
    # Hash the input password
    input_password = login_data.password
    input_hash = get_password_hash(input_password)
    
    # Verify password
    is_valid = verify_password(input_password, user.password)
    
    return {
        "debug_info": "⚠️ REMOVE THIS ENDPOINT IN PRODUCTION!",
        "email": user.email,
        "user_exists": True,
        "user_id": user.id,
        "is_active": user.is_active,
        "is_deleted": user.is_deleted,
        "password_check": {
            "input_password": input_password,
            "input_password_length": len(input_password),
            "new_hash_from_input": input_hash,
            "stored_hash_in_db": user.password,
            "stored_hash_length": len(user.password),
            "password_match": is_valid,
            "hash_algorithm": "bcrypt" if user.password.startswith("$2") else "unknown"
        },
        "result": "✅ Password CORRECT" if is_valid else "❌ Password WRONG"
    }


@router.get(
    "/debug/users",
    status_code=status.HTTP_200_OK,
    summary="Debug List Users (Development Only)",
    description="List all users in database - REMOVE IN PRODUCTION!",
    include_in_schema=True,
)
async def debug_list_users(
    db: AsyncSession = Depends(get_db),
):
    """
    ⚠️ DEVELOPMENT ONLY - REMOVE IN PRODUCTION!
    
    List all users for debugging.
    """
    from app.config import settings
    from sqlalchemy import select, func
    
    # Block in production
    if not settings.DEBUG:
        return {"error": "This endpoint is disabled in production"}
    
    # Get all users
    result = await db.execute(
        select(User).order_by(User.id)
    )
    users = result.scalars().all()
    
    # Get count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar()
    
    return {
        "debug_info": "⚠️ REMOVE THIS ENDPOINT IN PRODUCTION!",
        "total_users": total,
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "is_deleted": user.is_deleted,
                "password_hash_preview": user.password[:20] + "..." if user.password else None,
                "created_at": user.created_at
            }
            for user in users
        ]
    }