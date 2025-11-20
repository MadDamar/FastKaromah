from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, Tuple

from app.models.customer import Customer
from app.schemas.customer import CustomerSearchParams


class CustomerService:
    """Service class for customer operations"""
    
    @staticmethod
    async def search_customers(
        db: AsyncSession,
        search_params: CustomerSearchParams,
        store_id: int = 1
    ) -> Tuple[list[Customer], int]:
        """
        Search customers by multiple criteria with pagination.
        
        Args:
            db: Database session
            search_params: Search parameters
            
        Returns:
            Tuple of (customers list, total count)
        """
        # Base query
       
        query = select(Customer).where(Customer.store_id == store_id)
        count_query = select(func.count(Customer.id))
        
        # Apply filters
        filters = []
        
        # Search by name (case-insensitive partial match)
        if search_params.name:
            filters.append(Customer.name.ilike(f"%{search_params.name}%"))
        
        # Search by customer code
        if search_params.kode_cust:
            filters.append(Customer.kode_cust.ilike(f"%{search_params.kode_cust}%"))
        
        # Search by phone number
        if search_params.phone_number:
            filters.append(Customer.phone_number.ilike(f"%{search_params.phone_number}%"))
        
        # Search by email
        if search_params.email:
            filters.append(Customer.email.ilike(f"%{search_params.email}%"))
        
        # Filter by store_id
        if search_params.store_id is not None:
            filters.append(Customer.store_id == search_params.store_id)
        
        # Filter by active status
        if search_params.is_active is not None:
            filters.append(Customer.is_active == search_params.is_active)
        
        # Apply all filters
        if filters:
            query = query.where(*filters)
            count_query = count_query.where(*filters)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.page_size
        query = query.offset(offset).limit(search_params.page_size)
        
        # Order by name
        query = query.order_by(Customer.name.asc())
        
        # Execute query
        result = await db.execute(query)
        customers = result.scalars().all()
        
        return customers, total
    
    @staticmethod
    async def get_customer_by_id(
        db: AsyncSession,
        customer_id: int
    ) -> Optional[Customer]:
        """
        Get customer by ID.
        
        Args:
            db: Database session
            customer_id: Customer ID
            
        Returns:
            Customer object or None
        """
        result = await db.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_customer_by_kode(
        db: AsyncSession,
        kode_cust: str
    ) -> Optional[Customer]:
        """
        Get customer by customer code.
        
        Args:
            db: Database session
            kode_cust: Customer code
            
        Returns:
            Customer object or None
        """
        result = await db.execute(
            select(Customer).where(Customer.kode_cust == kode_cust)
        )
        return result.scalar_one_or_none()