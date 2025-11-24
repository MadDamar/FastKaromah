from sqlalchemy import String, Integer, Numeric, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.database import Base


class Sale(Base):
    """Sales table - hasil finalize transaksi"""
    __tablename__ = "sales"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference_no: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)
    biller_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_qty: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    total_discount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    total_tax: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    total_price: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    grand_total: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    order_tax_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    order_tax: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    order_discount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    coupon_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    coupon_discount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    shipping_cost: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    point_discount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    service_fee: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    sale_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    payment_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    paid_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    sale_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    staff_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    supervised: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    customer_alias: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_dikirim: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ProductSale(Base):
    """Product Sales table - detail item yang dijual"""
    __tablename__ = "product_sales"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference_no: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    variant_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    qty: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    sale_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    net_unit_price: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    discount: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    tax_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    tax: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    total: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    profit: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    taxed: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Payment(Base):
    """Payment table"""
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference_no: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    payment_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    paying: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    change: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    paying_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Balance(Base):
    """Balance table - track semua transaksi keuangan"""
    __tablename__ = "balance"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    jenis_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reff_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    jumlah: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    bayar: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    trx_id: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method_id: Mapped[int] = mapped_column(Integer, nullable=False)
    store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ProductLog(Base):
    """Product Logs - track pergerakan stock"""
    __tablename__ = "product_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_no: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_qty: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    end_qty: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    run_qty: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    status_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ProductWarehouse(Base):
    """Product Warehouse - stock per gudang"""
    __tablename__ = "product_warehouse"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    variant_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    qty: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class CustomerLog(Base):
    """Customer Logs - track transaksi customer"""
    __tablename__ = "customer_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    jenis_trx: Mapped[int] = mapped_column(Integer, nullable=False)
    jumlah: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    reff_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status_trx: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)