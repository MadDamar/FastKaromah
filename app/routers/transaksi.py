from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings
from app.schemas.transaksi import (
    TransaksiCreateRequest,
    TransaksiCreateResponse,
    TransaksiAddProductRequest,
    TransaksiAddProductResponse,
)
from app.models.user import User
from app.models.transaksi import TransaksiDetail
from app.services.transaksi_service import TransaksiService
from app.dependencies import get_current_active_user


router = APIRouter(prefix="/transaksi", tags=["Transaksi POS"])


@router.post("/create", response_model=TransaksiCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_transaksi(
    request: TransaksiCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Step 2: Operator membuat transaksi**
    
    Request:
    ```json
    {
      "customer_id": 15706,
      "jenis_trx": 1,
      "reference_sale": "",
      "warehouse_id": 1
    }
    ```
    
    Response:
    ```json
    {
      "success": true,
      "customer": {
        "name": "MafrukhatunNimah",
        "phone_number": "089538063336",
        "point": 5773710,
        "piutang": "0",
        "customer_group_id": 1
      },
      "id_transaksi": 300233
    }
    ```
    """
    transaksi_id, customer_info = await TransaksiService.create_transaksi(
        db=db,
        customer_id=request.customer_id,
        warehouse_id=request.warehouse_id,
        jenis_trx=request.jenis_trx,
        operator_id=current_user.id
    )
    
    if not transaksi_id:
        return TransaksiAddProductResponse(
            success=False,
            msg="Customer not found"
        )
    
    return TransaksiCreateResponse(
        success=True,
        customer=customer_info,
        id_transaksi=transaksi_id
    )


@router.post("/add-product", response_model=TransaksiAddProductResponse)
async def add_product_to_cart(
    request: TransaksiAddProductRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Step 4: Operator memasukkan barcode untuk add product**
    
    Request:
    ```json
    {
      "barcode": "ppp",
      "id_transaksi": 300233,
      "is_cabang": 1,
      "jumlah": 1,
      "warehouse_id": 1
    }
    ```
    
    Response (Success):
    ```json
    {
      "success": true,
      "dataproduk": [{
        "no": 1460165,
        "transaksi_id": 300233,
        "barcode": "ppp5",
        "product_id": 4833,
        "harga": 3300,
        "tax": 0,
        "hargatax": 3300,
        "nama": "Pluntir Polos Pendowo",
        "jumlah": 1,
        "unit": "PCS",
        "total": 3300,
        "diskon": 0,
        "profit": 0,
        "is_point": 1,
        "tax_rate": 0,
        "unit_id": 1
      }],
      "promo": null,
      "productproperties": []
    }
    ```
    
    Response (Error):
    ```json
    {
      "success": false,
      "msg": "Product not found"
    }
    ```
    """
    try:
        # 1. Get product by barcode
        product = await TransaksiService.get_product_by_barcode(
            db=db,
            barcode=request.barcode,
            store_id=current_user.store_id
        )
        
        if not product:
            return TransaksiAddProductResponse(
                success=False,
                msg="Product not found"
            )
        
        # 2. Get harga based on qty and customer group
        harga_data = await TransaksiService.get_harga(
            db=db,
            product_id=product.id,
            qty=request.jumlah,
            cust_group=request.is_cabang,
            warehouse_id=request.warehouse_id
        )
        
        if not harga_data:
            return TransaksiAddProductResponse(
                success=False,
                msg="Harga belum disetting"
            )
        
        # 3. Calculate price, tax, total
        calculation = TransaksiService.calculate_price(
            harga_data=harga_data,
            qty=request.jumlah,
            cust_group=request.is_cabang
        )
        
        # 4. Check if product already in cart
        existing_item = await TransaksiService.get_cart_item(
            db=db,
            transaksi_id=request.id_transaksi,
            barcode=product.barcode
        )
        
        if existing_item:
            # UPDATE: Product sudah ada, tambah quantity
            new_qty = existing_item.jumlah + request.jumlah
            
            # Recalculate dengan qty baru (karena harga bisa berubah berdasarkan qty)
            new_harga = await TransaksiService.get_harga(
                db=db,
                product_id=product.id,
                qty=new_qty,
                cust_group=request.is_cabang,
                warehouse_id=request.warehouse_id
            )
            
            new_calculation = TransaksiService.calculate_price(
                harga_data=new_harga,
                qty=new_qty,
                cust_group=request.is_cabang
            )
            
            existing_item.jumlah = new_qty
            existing_item.harga = new_calculation['harganet']
            existing_item.tax = new_calculation['pajak']
            existing_item.total = new_calculation['total_harga']
            existing_item.profit = new_calculation['profit']
            
        else:
            # INSERT: Product baru di cart
            new_item = TransaksiDetail(
                transaksi_id=request.id_transaksi,
                barcode=product.barcode,
                nama=product.name,
                product_id=product.id,
                jumlah=request.jumlah,
                unit=harga_data['unit_name'],
                harga=calculation['harganet'],
                diskon=0,
                total=calculation['total_harga'],
                is_point=product.is_point or 0,
                tax_rate=calculation['tax_rate'],
                tax=calculation['pajak'],
                profit=calculation['profit'],
                unit_id=harga_data['unit_id']
            )
            db.add(new_item)
        
        await db.commit()
        
        # 5. Check promo
        promo = await TransaksiService.check_promo(db, product.id)
        promo_data = None
        if promo:
            promo_data = {
                "promotion_price": float(promo.promotion_price),
                "max_item_promo": promo.max_item_promo
            }
        
        # 6. Get all cart items
        cart_items = await TransaksiService.get_all_cart_items(db, request.id_transaksi)
        dataproduk = TransaksiService.format_cart_items(cart_items)
        
        return TransaksiAddProductResponse(
            success=True,
            dataproduk=dataproduk,
            promo=promo_data,
            productproperties=[]
        )
        
    except Exception as e:
        await db.rollback()
        import traceback
        
        # Get detailed error info
        error_traceback = traceback.format_exc()
        error_lines = error_traceback.split('\n')
        
        # Find the specific line that caused error
        error_location = "Unknown"
        for line in error_lines:
            if 'File "' in line and 'transaksi' in line.lower():
                error_location = line.strip()
                break
        
        detailed_error = {
            "error": str(e),
            "type": type(e).__name__,
            "location": error_location,
            "full_traceback": error_traceback if settings.DEBUG else None
        }
        
        print(f"\n❌ Error in add_product_to_cart:")
        print(f"   Error: {str(e)}")
        print(f"   Location: {error_location}")
        if settings.DEBUG:
            print(f"\n{error_traceback}\n")
        
        return TransaksiAddProductResponse(
            success=False,
            msg=f"Error: {str(e)} | Location: {error_location}"
        )


@router.get("/{transaksi_id}/cart", response_model=TransaksiAddProductResponse)
async def get_cart(
    transaksi_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Get semua item di cart**
    
    Response sama seperti add-product
    """
    try:
        cart_items = await TransaksiService.get_all_cart_items(db, transaksi_id)
        dataproduk = TransaksiService.format_cart_items(cart_items)
        
        return TransaksiAddProductResponse(
            success=True,
            dataproduk=dataproduk,
            promo=None,
            productproperties=[]
        )
    except Exception as e:
        return TransaksiAddProductResponse(
            success=False,
            msg=f"Error: {str(e)}"
        )


@router.delete("/{transaksi_id}/product/{barcode}")
async def delete_product_from_cart(
    transaksi_id: int,
    barcode: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Hapus product dari cart**
    """
    try:
        item = await TransaksiService.get_cart_item(db, transaksi_id, barcode)
        
        if not item:
            return TransaksiAddProductResponse(
                success=False,
                msg="Product not found in cart"
            )
        
        await db.delete(item)
        await db.commit()
        
        # Get updated cart
        cart_items = await TransaksiService.get_all_cart_items(db, transaksi_id)
        dataproduk = TransaksiService.format_cart_items(cart_items)
        
        return TransaksiAddProductResponse(
            success=True,
            msg="Product deleted",
            dataproduk=dataproduk,
            promo=None,
            productproperties=[]
        )
        
    except Exception as e:
        await db.rollback()
        import traceback
        error_traceback = traceback.format_exc()
        print(f"\n❌ Error in delete_product: {str(e)}\n{error_traceback}\n")
        
        return TransaksiAddProductResponse(
            success=False,
            msg=f"Error: {str(e)}"
        )


@router.put("/update-product", response_model=TransaksiAddProductResponse)
async def update_product_quantity(
    request: TransaksiAddProductRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Update quantity product di cart**
    
    Harga akan otomatis recalculate karena bisa berubah based on quantity.
    Jika jumlah = 0, product akan dihapus dari cart.
    
    Request:
    ```json
    {
      "barcode": "ppp",
      "id_transaksi": 300233,
      "is_cabang": 1,
      "jumlah": 5,
      "warehouse_id": 1
    }
    ```
    
    Response: sama seperti add-product
    """
    try:
        # 1. Get existing item
        existing_item = await TransaksiService.get_cart_item(
            db=db,
            transaksi_id=request.id_transaksi,
            barcode=request.barcode
        )
        
        if not existing_item:
            return TransaksiAddProductResponse(
                success=False,
                msg="Product not found in cart"
            )
        
        # 2. Jika jumlah = 0, hapus dari cart
        if request.jumlah <= 0:
            await db.delete(existing_item)
            await db.commit()
            
            # Get updated cart
            cart_items = await TransaksiService.get_all_cart_items(db, request.id_transaksi)
            dataproduk = TransaksiService.format_cart_items(cart_items)
            
            return TransaksiAddProductResponse(
                success=True,
                msg="Product deleted (quantity = 0)",
                dataproduk=dataproduk,
                promo=None,
                productproperties=[]
            )
        
        # 3. Update quantity - Recalculate harga based on new qty
        # Get product info
        product = await TransaksiService.get_product_by_barcode(
            db=db,
            barcode=request.barcode,
            store_id=current_user.store_id
        )
        
        if not product:
            return TransaksiAddProductResponse(
                success=False,
                msg="Product not found"
            )
        
        # 4. Get harga based on NEW quantity (PENTING: harga bisa beda!)
        harga_data = await TransaksiService.get_harga(
            db=db,
            product_id=product.id,
            qty=request.jumlah,
            cust_group=request.is_cabang,
            warehouse_id=request.warehouse_id
        )
        
        if not harga_data:
            return TransaksiAddProductResponse(
                success=False,
                msg="Harga belum disetting"
            )
        
        # 5. Calculate dengan qty baru
        calculation = TransaksiService.calculate_price(
            harga_data=harga_data,
            qty=request.jumlah,
            cust_group=request.is_cabang
        )
        
        # 6. Update item
        existing_item.jumlah = request.jumlah
        existing_item.harga = calculation['harganet']
        existing_item.tax = calculation['pajak']
        existing_item.total = calculation['total_harga']
        existing_item.profit = calculation['profit']
        existing_item.tax_rate = calculation['tax_rate']
        
        await db.commit()
        
        # 7. Check promo
        promo = await TransaksiService.check_promo(db, product.id)
        promo_data = None
        if promo:
            promo_data = {
                "promotion_price": float(promo.promotion_price),
                "max_item_promo": promo.max_item_promo
            }
        
        # 8. Get updated cart
        cart_items = await TransaksiService.get_all_cart_items(db, request.id_transaksi)
        dataproduk = TransaksiService.format_cart_items(cart_items)
        
        return TransaksiAddProductResponse(
            success=True,
            msg="Product quantity updated",
            dataproduk=dataproduk,
            promo=promo_data,
            productproperties=[]
        )
        
    except Exception as e:
        await db.rollback()
        import traceback
        
        error_traceback = traceback.format_exc()
        error_lines = error_traceback.split('\n')
        
        error_location = "Unknown"
        for line in error_lines:
            if 'File "' in line and 'transaksi' in line.lower():
                error_location = line.strip()
                break
        
        print(f"\n❌ Error in update_product_quantity:")
        print(f"   Error: {str(e)}")
        print(f"   Location: {error_location}")
        if settings.DEBUG:
            print(f"\n{error_traceback}\n")
        
        return TransaksiAddProductResponse(
            success=False,
            msg=f"Error: {str(e)} | Location: {error_location}"
        )