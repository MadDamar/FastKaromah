from pydantic import BaseModel, Field
from typing import Optional


class CheckoutRequest(BaseModel):
    """Request untuk finalize/checkout transaksi"""
    id_transaksi: int = Field(..., description="ID Transaksi yang akan di-checkout")
    paying_method: int = Field(..., description="Payment method ID (1=Cash, 6=COD, dll)")
    paying_amount: float = Field(..., ge=0, description="Jumlah uang yang dibayar")
    order_discount: float = Field(default=0, description="Diskon order level")
    shipping_cost: float = Field(default=0, description="Ongkos kirim")
    service_fee: float = Field(default=0, description="Biaya layanan")
    order_tax: float = Field(default=0, description="Pajak order level")
    order_tax_rate: float = Field(default=0, description="Rate pajak order")
    point: float = Field(default=0, description="Point yang digunakan")
    coupon_id: Optional[str] = Field(None, description="Kode kupon (jika ada)")
    sale_note: Optional[str] = Field(None, description="Catatan penjualan")
    staff_note: Optional[str] = Field(None, description="Catatan staff")
    supervised: Optional[int] = Field(None, description="ID supervisor")
    customer_alias: Optional[str] = Field(None, description="Alias nama customer")
    is_dikirim: int = Field(default=0, description="1=COD/dikirim, 0=langsung")


class CheckoutResponse(BaseModel):
    """Response setelah checkout"""
    success: bool
    msg: Optional[str] = None
    sale_id: Optional[int] = None
    grand_total: Optional[float] = None
    paying_amount: Optional[float] = None
    change: Optional[float] = None
    piutang: Optional[float] = None
    reference_no: Optional[str] = None