from pydantic import BaseModel, Field
from typing import Optional, List


# ==================== REQUEST SCHEMAS ====================

class TransaksiCreateRequest(BaseModel):
    """Request untuk membuat transaksi baru"""
    customer_id: int = Field(..., description="ID Customer")
    jenis_trx: int = Field(..., description="Jenis transaksi (1=penjualan)")
    reference_sale: str = Field(default="", description="Reference sale number")
    warehouse_id: int = Field(..., description="ID Warehouse")


class TransaksiAddProductRequest(BaseModel):
    """Request untuk menambah product ke cart"""
    barcode: str = Field(..., description="Barcode product")
    id_transaksi: int = Field(..., description="ID Transaksi")
    is_cabang: int = Field(default=1, description="Customer group: 0=gudang, 1=umum, 2=cabang")
    jumlah: float = Field(..., gt=0, description="Jumlah/quantity product")
    warehouse_id: int = Field(..., description="ID Warehouse")


# ==================== RESPONSE SCHEMAS ====================

class CustomerInfoResponse(BaseModel):
    """Response info customer"""
    name: str
    phone_number: Optional[str] = None
    point: float = 0
    piutang: str = "0"
    customer_group_id: Optional[int] = None


class TransaksiCreateResponse(BaseModel):
    """Response setelah create transaksi"""
    success: bool
    customer: CustomerInfoResponse
    id_transaksi: int


class ProductInCartResponse(BaseModel):
    """Response detail product di cart"""
    no: int
    transaksi_id: int
    barcode: str
    product_id: int
    harga: float
    tax: float
    hargatax: float
    nama: str
    jumlah: float
    unit: str
    total: float
    diskon: float = 0
    profit: float = 0
    is_point: int = 0
    tax_rate: float = 0
    unit_id: int


class TransaksiAddProductResponse(BaseModel):
    """Response setelah add/update product"""
    success: bool
    msg: Optional[str] = None
    dataproduk: Optional[List[ProductInCartResponse]] = None
    promo: Optional[dict] = None
    productproperties: List = []