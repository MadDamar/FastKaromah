from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from typing import Optional, Dict, List
import random
import string

from app.models.transaksi import Transaksi, TransaksiDetail
from app.models.sales import Sale, ProductSale, Payment, Balance, ProductLog, ProductWarehouse, CustomerLog
from app.models.customer import Customer


class CheckoutService:
    """Service untuk handle checkout/finalize transaksi"""
    
    @staticmethod
    def generate_reference_no(jenis_trx: int) -> str:
        """Generate reference number untuk sale"""
        now = datetime.now()
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        
        if jenis_trx == 1:  # Penjualan
            return f"P{now.strftime('%y%m%d')}-{now.strftime('%H%M%S')}{random_str}"
        elif jenis_trx == 5:  # Retur
            return f"R{now.strftime('%y%m%d')}-{now.strftime('%H%M%S')}"
        else:
            return f"S{now.strftime('%y%m%d')}-{now.strftime('%H%M%S')}"
    
    @staticmethod
    def generate_payment_reference() -> str:
        """Generate payment reference number"""
        now = datetime.now()
        return f"spr-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
    
    @staticmethod
    def get_payment_method_name(method_id: int) -> str:
        """Convert payment method ID to name"""
        methods = {
            1: "Cash",
            2: "Ovo",
            3: "Gopay", 
            4: "Shopee",
            5: "Transfer",
            6: "COD",
            7: "QRIS"
        }
        return methods.get(method_id, "Cash")
    
    @staticmethod
    async def get_transaksi_summary(
        db: AsyncSession,
        transaksi_id: int
    ) -> Optional[Dict]:
        """Get summary total dari transaksi_detail"""
        result = await db.execute(
            select(
                func.count(TransaksiDetail.no).label('item'),
                func.sum(TransaksiDetail.total).label('total'),
                func.sum(TransaksiDetail.jumlah).label('qty'),
                func.sum(TransaksiDetail.tax).label('total_tax'),
                func.sum(TransaksiDetail.diskon).label('total_discount'),
                func.sum(TransaksiDetail.profit).label('total_profit')
            ).where(TransaksiDetail.transaksi_id == transaksi_id)
        )
        
        row = result.first()
        if not row or row.item == 0:
            return None
        
        return {
            "item": row.item,
            "total_price": float(row.total or 0),
            "total_qty": float(row.qty or 0),
            "total_tax": float(row.total_tax or 0),
            "total_discount": float(row.total_discount or 0),
            "total_profit": float(row.total_profit or 0)
        }
    
    @staticmethod
    async def create_sale(
        db: AsyncSession,
        transaksi: Transaksi,
        summary: Dict,
        checkout_data: Dict,
        reference_no: str,
        grand_total: float,
        payment_status: str,
        operator_id: int,
        store_id: int
    ) -> int:
        """Create record di table sales"""
        now = datetime.now(timezone.utc)
        
        sale = Sale(
            reference_no=reference_no,
            store_id=store_id,
            warehouse_id=transaksi.warehouse_id,
            biller_id=transaksi.biller_id or 1,
            customer_id=transaksi.customer_id,
            user_id=operator_id,
            item=summary['item'],
            total_qty=summary['total_qty'],
            total_discount=summary['total_discount'],
            total_tax=summary['total_tax'],
            total_price=summary['total_price'],
            grand_total=grand_total,
            order_tax=checkout_data['order_tax'],
            order_tax_rate=checkout_data['order_tax_rate'],
            order_discount=checkout_data['order_discount'],
            shipping_cost=checkout_data['shipping_cost'],
            service_fee=checkout_data['service_fee'],
            point_discount=checkout_data['point'],
            coupon_id=None,  # TODO: handle coupon
            coupon_discount=0,
            sale_status='1',
            payment_status=payment_status,
            paid_amount=checkout_data['paid_amount'],
            sale_note=checkout_data.get('sale_note'),
            staff_note=checkout_data.get('staff_note'),
            supervised=checkout_data.get('supervised'),
            customer_alias=checkout_data.get('customer_alias'),
            is_dikirim=checkout_data.get('is_dikirim', 0),
            created_at=now,
            updated_at=now
        )
        
        db.add(sale)
        await db.flush()
        
        return sale.id
    
    @staticmethod
    async def create_product_sales(
        db: AsyncSession,
        transaksi_id: int,
        reference_no: str,
        store_id: int,
        warehouse_id: int
    ) -> List[Dict]:
        """Copy transaksi_detail ke product_sales dan update stock"""
        now = datetime.now(timezone.utc)
        
        # Get all transaksi detail
        result = await db.execute(
            select(TransaksiDetail).where(
                TransaksiDetail.transaksi_id == transaksi_id
            )
        )
        details = result.scalars().all()
        
        results = []
        
        for detail in details:
            # Create product sale
            product_sale = ProductSale(
                reference_no=reference_no,
                product_id=detail.product_id,
                qty=detail.jumlah,
                sale_unit_id=detail.unit_id,
                net_unit_price=detail.harga,
                discount=detail.diskon or 0,
                tax_rate=detail.tax_rate or 0,
                tax=detail.tax or 0,
                total=detail.total,
                profit=detail.profit or 0,
                taxed=0,
                created_at=now,
                updated_at=now
            )
            db.add(product_sale)
            
            # Update product warehouse stock
            stock_result = await db.execute(
                select(ProductWarehouse).where(
                    ProductWarehouse.product_id == detail.product_id,
                    ProductWarehouse.warehouse_id == warehouse_id
                )
            )
            product_warehouse = stock_result.scalar_one_or_none()
            
            if product_warehouse:
                old_qty = float(product_warehouse.qty)
                new_qty = old_qty - float(detail.jumlah)
                product_warehouse.qty = new_qty
                product_warehouse.updated_at = now
                
                # Create product log
                product_log = ProductLog(
                    store_id=store_id,
                    reference_no=reference_no,
                    warehouse_id=warehouse_id,
                    product_id=detail.product_id,
                    start_qty=old_qty,
                    end_qty=new_qty,
                    run_qty=float(detail.jumlah),
                    status_qty=1,  # 1 = Penjualan
                    created_at=now
                )
                db.add(product_log)
                
                results.append({
                    "product_id": detail.product_id,
                    "old_stock": old_qty,
                    "new_stock": new_qty,
                    "qty_sold": float(detail.jumlah)
                })
        
        return results
    
    @staticmethod
    async def create_payment(
        db: AsyncSession,
        reference_no: str,
        payment_method_id: int,
        paid_amount: float,
        paying_amount: float,
        payment_note: Optional[str],
        operator_id: int,
        store_id: int
    ) -> bool:
        """Create payment record"""
        now = datetime.now(timezone.utc)
        payment_reference = CheckoutService.generate_payment_reference()
        payment_method = CheckoutService.get_payment_method_name(payment_method_id)
        change = paying_amount - paid_amount
        
        payment = Payment(
            reference_no=reference_no,
            payment_reference=payment_reference,
            user_id=operator_id,
            account_id=1,  # Default account
            paying=paying_amount,
            amount=paid_amount,
            change=change,
            paying_method=payment_method,
            payment_note=payment_note,
            store_id=store_id,
            created_at=now,
            updated_at=now
        )
        
        db.add(payment)
        return True
    
    @staticmethod
    async def create_balance_entry(
        db: AsyncSession,
        jenis_id: int,
        reference_no: str,
        user_id: int,
        customer_id: int,
        jumlah: float,
        bayar: float,
        trx_id: int,
        payment_method_id: int,
        store_id: int,
        warehouse_id: int
    ) -> bool:
        """Create balance/ledger entry"""
        now = datetime.now(timezone.utc)
        
        balance = Balance(
            jenis_id=jenis_id,
            reff_number=reference_no,
            user_id=user_id,
            customer_id=customer_id,
            jumlah=jumlah,
            bayar=bayar,
            trx_id=trx_id,
            payment_method_id=payment_method_id,
            store_id=store_id,
            warehouse_id=warehouse_id,
            created_at=now,
            updated_at=now
        )
        
        db.add(balance)
        return True
    
    @staticmethod
    async def create_customer_log(
        db: AsyncSession,
        customer_id: int,
        jenis_trx: int,
        jumlah: float,
        reff_id: int,
        store_id: int,
        status_trx: int = 1
    ) -> bool:
        """Create customer transaction log"""
        now = datetime.now(timezone.utc)
        
        cust_log = CustomerLog(
            customer_id=customer_id,
            jenis_trx=jenis_trx,
            jumlah=jumlah,
            reff_id=reff_id,
            status_trx=status_trx,
            store_id=store_id,
            created_at=now,
            updated_at=now
        )
        
        db.add(cust_log)
        return True