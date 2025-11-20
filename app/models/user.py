from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.database import Base


class User(Base):
    """User model compatible with Laravel users table"""
    
    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Optional fields from Laravel
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    biller_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    warehouse_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    store_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Status fields
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Auth fields
    remember_token: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    auth_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps (Laravel default)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"