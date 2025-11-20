from sqlalchemy import String, Integer, Numeric, Date, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from app.database import Base


class Customer(Base):
    """Customer model compatible with Laravel customers table"""
    
    __tablename__ = "customers"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    nik: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Contact info
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    
    # Tax & Business
    tax_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    customer_group_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Address
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    kecamatan_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    kelurahan_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Financial
    deposit: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), default=0, nullable=True)
    expense: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), default=0, nullable=True)
    
    # Status & Store
    is_active: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    kode_cust: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    store_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    
    # OTP for verification
    otp: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # Timestamps (Laravel default) - as string to handle invalid dates
    created_at: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, name={self.name}, kode_cust={self.kode_cust})>"
    
    @property
    def is_active_bool(self) -> bool:
        """Convert is_active to boolean"""
        return bool(self.is_active) if self.is_active is not None else True
    
    @property
    def tgl_lhr_date(self) -> Optional[date]:
        """Convert tgl_lhr string to date, return None if invalid"""
        if not self.tgl_lhr or self.tgl_lhr == '0000-00-00':
            return None
        try:
            return datetime.strptime(self.tgl_lhr, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None