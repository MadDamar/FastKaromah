from sqlalchemy import String, Integer, Numeric, DateTime, Text, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from app.database import Base



class Transaksi(Base):
    """Transaksi model - sesuai dengan Laravel Transaksi"""
    __tablename__ = "transaksi"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)
    biller_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sale_status: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    operator_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tgl_transaksi: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    payment_method_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    jenis_trx: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reference_sale: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_online: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)


class TransaksiDetail(Base):
    """TransaksiDetail model - sesuai dengan Laravel TransaksiDetail"""
    __tablename__ = "transaksi_detail"
    
    no: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaksi_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    barcode: Mapped[str] = mapped_column(String(100), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nama: Mapped[str] = mapped_column(String(255), nullable=False)
    jumlah: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    harga: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    total: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    diskon: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True, default=0)
    profit: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    is_point: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    tax_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True, default=0)
    tax: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True, default=0)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)

class Product(Base):
    """Product model - sesuai dengan Laravel Product"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_lbl: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    barcode: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    barcode_symbology: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    brand_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    unit_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    purchase_unit_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sale_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    margin: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    qty: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    alert_quantity: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    promotion: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    promotion_price: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    max_item_promo: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    starting_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    tax_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tax_method: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_variant: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    featured: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    product_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qty_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    product_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    is_autoupdate: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    is_point: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    is_toped: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    is_shopee: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    last_adjustment: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expired: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    store_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ProductPrice(Base):
    """ProductPrice model - sesuai dengan Laravel ProductPrice"""
    __tablename__ = "product_prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    minimal: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    harga: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    margin: Mapped[Optional[float]] = mapped_column(Numeric(20, 2), nullable=True)
    percent: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Unit(Base):
    """Unit model - sesuai dengan Laravel Unit"""
    __tablename__ = "units"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_code: Mapped[str] = mapped_column(String(20), nullable=False)
    unit_name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_unit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    operator: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    operation_value: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Tax(Base):
    """Tax model - sesuai dengan Laravel Tax"""
    __tablename__ = "taxes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rate: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    store_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)