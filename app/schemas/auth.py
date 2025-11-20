from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Request Schemas
class UserRegister(BaseModel):
    """User registration request schema"""
    name: str = Field(..., min_length=2, max_length=255, description="User full name")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")


class UserLogin(BaseModel):
    """User login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


# Response Schemas
class UserResponse(BaseModel):
    """User response schema (without sensitive data)"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    role_id: Optional[int] = None
    biller_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    store_id: Optional[int] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Token response schema (Laravel Sanctum compatible)"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class AuthResponse(BaseModel):
    """Authentication response with user and token"""
    user: UserResponse
    token: TokenResponse


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str