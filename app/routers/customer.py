from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas.customer import (
    CustomerResponse,
    CustomerListResponse,
    CustomerSearchParams,
)
from app.models.user import User
from app.services.customer_service import CustomerService
from app.dependencies import get_current_active_user


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get(
    "/search",
    response_model=CustomerListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search customers",
    description="Search customers by name, code, phone, or email with pagination",
)
async def search_customers(
    name: Optional[str] = Query(None, description="Search by customer name"),
    kode_cust: Optional[str] = Query(None, description="Search by customer code"),
    phone_number: Optional[str] = Query(None, description="Search by phone number"),
    email: Optional[str] = Query(None, description="Search by email"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    is_active: Optional[int] = Query(1, description="Filter by active status (1=active, 0=inactive)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    
    # Create search params
    search_params = CustomerSearchParams(
        name=name,
        kode_cust=kode_cust,
        phone_number=phone_number,
        email=email,
        store_id=store_id,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )
    
    # Search customers
    customers, total = await CustomerService.search_customers(db, search_params,current_user.store_id)
    
    return CustomerListResponse(
        total=total,
        page=page,
        page_size=page_size,
        customers=[CustomerResponse.model_validate(c) for c in customers],
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get customer by ID",
    description="Get detailed customer information by ID",
)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get customer by ID.
    
    **Path Parameters:**
    - **customer_id**: Customer ID
    """
    customer = await CustomerService.get_customer_by_id(db, customer_id)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return CustomerResponse.model_validate(customer)


@router.get(
    "/code/{kode_cust}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get customer by code",
    description="Get customer information by customer code",
)
async def get_customer_by_code(
    kode_cust: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get customer by customer code.
    
    **Path Parameters:**
    - **kode_cust**: Customer code
    """
    customer = await CustomerService.get_customer_by_kode(db, kode_cust)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return CustomerResponse.model_validate(customer)