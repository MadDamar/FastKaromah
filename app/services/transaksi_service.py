from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, List
from app.models.transaksi import Transaksi, TransaksiDetail, Product
from app.models.customer import Customer


class TransaksiService:
    """Service untuk handle business logic transaksi"""
    
    @staticmethod
    async def create_transaksi(
        db: AsyncSession,
        customer_id: int,
        warehouse_id: int,
        jenis_trx: int,
        operator_id: int
    ) -> Tuple[Optional[int], Optional[Dict]]:
        """
        Step 2: Create transaksi header
        Sama seperti Laravel: Transaksi::create()
        """
        # Get customer info
        result = await db.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        customer = result.scalar_one_or_none()
        
        if not customer:
            return None, None
        
        # Create transaksi
        now = datetime.now(timezone.utc)
        transaksi = Transaksi(
            warehouse_id=warehouse_id,
            biller_id=1,
            customer_id=customer_id,
            operator_id=operator_id,
            sale_status='0',
            jenis_trx=jenis_trx,
            is_online=0,
            tgl_transaksi=now
        )
        
        db.add(transaksi)
        await db.commit()
        await db.refresh(transaksi)
        
        # Customer info response
        customer_info = {
            "name": customer.name,
            "phone_number": customer.phone_number,
            "point": float(customer.deposit or 0),
            "piutang": str(customer.expense or 0),
            "customer_group_id": customer.customer_group_id
        }
        
        return transaksi.id, customer_info
    
    @staticmethod
    async def get_product_by_barcode(
        db: AsyncSession,
        barcode: str,
        store_id: int
    ) -> Optional[Product]:
        """
        Get product by barcode or code
        Sama seperti Laravel: getproduct($store_id, $barcode)
        """
        result = await db.execute(
            select(Product).where(
                Product.store_id == store_id,
                ((Product.barcode == barcode) | (Product.code == barcode))
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_harga(
        db: AsyncSession,
        product_id: int,
        qty: float,
        cust_group: int,
        warehouse_id: int
    ) -> Optional[Dict]:
        """
        Get harga product berdasarkan qty dan customer group
        Sama seperti Laravel: GetHarga($product_id, $qty, $cust_group, $warehouse_id)
        """
        qty = abs(qty)
        
        if cust_group == 1:  # Umum (retail) - pakai product_prices
            query = text("""
                SELECT T1.*, MIN(pp.harga) as price 
                FROM (
                    SELECT p.id, p.barcode, p.name, p.id as product_id, p.is_point,
                           u.unit_name, u.id as unit_id, p.cost, 
                           COALESCE(t.rate, 0) as tax_rate, p.tax_method, p.tax_id
                    FROM products p
                    LEFT JOIN units u ON u.id = p.sale_unit_id
                    LEFT JOIN taxes t ON p.tax_id = t.id
                    WHERE p.id = :product_id
                ) as T1
                INNER JOIN product_prices pp ON T1.id = pp.product_id
                WHERE pp.warehouse_id = :warehouse_id 
                AND pp.minimal <= :min
            """)
            
            result = await db.execute(
                query,
                {"product_id": product_id, "min": qty, "warehouse_id": warehouse_id}
            )
            
        else:  # Cabang/Gudang (2/3) - pakai cost
            query = text("""
                SELECT p.barcode, p.name, p.id as product_id, p.is_point,
                       p.cost as price, u.unit_name, u.id as unit_id, p.cost,
                       COALESCE(t.rate, 0) as tax_rate, p.tax_method, p.tax_id
                FROM products p
                LEFT JOIN units u ON u.id = p.sale_unit_id
                LEFT JOIN taxes t ON p.tax_id = t.id
                WHERE p.id = :product_id
            """)
            
            result = await db.execute(query, {"product_id": product_id})
        
        row = result.first()
        return dict(row._mapping) if row else None
    
    @staticmethod
    def calculate_price(
        harga_data: Dict,
        qty: float,
        cust_group: int
    ) -> Dict:
        """
        Calculate harga, tax, total
        Sama seperti di Laravel InsertCart/UpdateCart
        """
        # Convert all to float to avoid Decimal issues
        tax_rate = float(harga_data.get('tax_rate', 0) or 0)
        base_price = float(harga_data.get('price', 0))
        cost = float(harga_data.get('cost', 0))
        tax_method = harga_data.get('tax_method')
        qty = float(qty)
        
        if cust_group == 1:  # Umum
            if tax_method == "1":  # Exclude tax
                harganet = base_price
                pajak = round((harganet * (tax_rate / 100)) * qty, 2)
                total_harga = (harganet * qty) + pajak
            else:  # Include tax
                harganet = (100 / (100 + tax_rate)) * base_price
                pajak = round((base_price - harganet) * qty, 2)
                total_harga = base_price * qty
        else:  # Cabang/Gudang
            harganet = base_price
            tax_rate = 0
            pajak = 0
            total_harga = base_price * qty
        
        profit = round(qty * (harganet - cost), 2)
        
        return {
            "harganet": round(harganet, 2),
            "pajak": pajak,
            "total_harga": round(total_harga, 2),
            "profit": profit,
            "tax_rate": tax_rate
        }
    
    @staticmethod
    async def check_promo(
        db: AsyncSession,
        product_id: int
    ) -> Optional[Product]:
        """Check apakah product sedang promo"""
        now = datetime.now(timezone.utc)
        
        result = await db.execute(
            select(Product).where(
                Product.id == product_id,
                Product.promotion == 1,
                Product.starting_date <= now,
                Product.last_date >= now
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_cart_item(
        db: AsyncSession,
        transaksi_id: int,
        barcode: str
    ) -> Optional[TransaksiDetail]:
        """Get item yang sudah ada di cart"""
        result = await db.execute(
            select(TransaksiDetail).where(
                TransaksiDetail.transaksi_id == transaksi_id,
                TransaksiDetail.barcode == barcode
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_cart_items(
        db: AsyncSession,
        transaksi_id: int
    ) -> List[TransaksiDetail]:
        """Get semua item di cart"""
        result = await db.execute(
            select(TransaksiDetail)
            .where(TransaksiDetail.transaksi_id == transaksi_id)
            .order_by(TransaksiDetail.no.asc())
        )
        return result.scalars().all()
    
    @staticmethod
    def format_cart_items(items: List[TransaksiDetail]) -> List[Dict]:
        """Format cart items untuk response"""
        result = []
        for item in items:
            hargatax = float(item.harga) + (float(item.tax) / float(item.jumlah) if item.jumlah > 0 else 0)
            result.append({
                "no": item.no,
                "transaksi_id": item.transaksi_id,
                "barcode": item.barcode,
                "product_id": item.product_id,
                "harga": float(item.harga),
                "tax": float(item.tax or 0),
                "hargatax": round(hargatax, 2),
                "nama": item.nama,
                "jumlah": float(item.jumlah),
                "unit": item.unit,
                "total": float(item.total),
                "diskon": float(item.diskon or 0),
                "profit": float(item.profit or 0),
                "is_point": item.is_point or 0,
                "tax_rate": float(item.tax_rate or 0),
                "unit_id": item.unit_id
            })
        return result
    