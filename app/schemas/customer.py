from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class CustomerBase(BaseModel):
    """Base customer schema"""
    name: str
    nik: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    tax_no: Optional[str] = None
    customer_group_id: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    kecamatan_id: Optional[int] = None
    kelurahan_id: Optional[int] = None
    state: Optional[str] = None
    deposit: Optional[float] = None
    expense: Optional[float] = None
    is_active: Optional[int] = None
    kode_cust: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Customer response schema"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class CustomerListResponse(BaseModel):
    """Customer list response with pagination"""
    total: int
    page: int
    page_size: int
    customers: list[CustomerResponse]


class CustomerSearchParams(BaseModel):
    """Customer search parameters"""
    name: Optional[str] = Field(None, description="Search by customer name (partial match)")
    kode_cust: Optional[str] = Field(None, description="Search by customer code")
    phone_number: Optional[str] = Field(None, description="Search by phone number")
    email: Optional[str] = Field(None, description="Search by email")
    store_id: Optional[int] = Field(None, description="Filter by store ID")
    is_active: Optional[int] = Field(1, description="Filter by active status (1=active, 0=inactive)")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")