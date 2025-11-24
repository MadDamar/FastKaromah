from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,text

from app.database import get_db
from app.config import settings
from app.schemas.checkout import CheckoutRequest, CheckoutResponse
from app.models.user import User
from app.models.transaksi import Transaksi
from app.services.checkout_service import CheckoutService
from app.dependencies import get_current_active_user


router = APIRouter(prefix="/checkout", tags=["Checkout & Payment"])


@router.post("/finalize", response_model=CheckoutResponse)
async def finalize_transaction(
    request: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    **Finalize/Checkout Transaksi**
    
    Memproses cart (transaksi & transaksi_detail) menjadi sale final:
    1. Validate transaksi exists dan belum diproses
    2. Calculate grand total
    3. Create sale record
    4. Copy transaksi_detail → product_sales
    5. Update product stock (product_warehouse)
    6. Create product logs
    7. Create payment record
    8. Create balance entries
    9. Create customer logs
    10. Delete transaksi & transaksi_detail (cart)
    
    Request:
    ```json
    {
      "id_transaksi": 300233,
      "paying_method": 1,
      "paying_amount": 50000,
      "order_discount": 0,
      "shipping_cost": 10000,
      "service_fee": 0,
      "order_tax": 0,
      "order_tax_rate": 0,
      "point": 0,
      "coupon_id": null,
      "sale_note": "Terima kasih",
      "staff_note": "",
      "supervised": null,
      "customer_alias": null,
      "is_dikirim": 0
    }
    ```
    
    Response:
    ```json
    {
      "success": true,
      "msg": "Transaksi berhasil",
      "sale_id": 12345,
      "reference_no": "P250113-143025abc",
      "grand_total": 45000,
      "paying_amount": 50000,
      "change": 5000,
      "piutang": 0
    }
    ```
    """
    try:
        # 1. Validate transaksi
        transaksi_result = await db.execute(
            select(Transaksi).where(
                Transaksi.id == request.id_transaksi,
                Transaksi.sale_status == '0'  # Belum diproses
            )
        )
        transaksi = transaksi_result.scalar_one_or_none()
        
        if not transaksi:
            return CheckoutResponse(
                success=False,
                msg="Transaksi tidak ditemukan atau sudah diproses"
            )
        
        # 2. Get cart summary
        summary = await CheckoutService.get_transaksi_summary(db, request.id_transaksi)
        
        if not summary:
            return CheckoutResponse(
                success=False,
                msg="Tidak ada produk di cart"
            )
        
        # 3. Calculate totals
        total_price = summary['total_price']
        
        # Bulatkan ke bawah ratusan
        total_price_rounded = (int(total_price) // 100) * 100
        
        # Handle point (jika digunakan, jadi negatif)
        point_discount = -abs(request.point) if request.point > 0 else 0
        
        # Handle order discount (jadi negatif)
        order_discount = -abs(request.order_discount) if request.order_discount > 0 else 0
        
        # Calculate grand total
        grand_total = (
            total_price_rounded +
            request.shipping_cost +
            request.service_fee +
            request.order_tax +
            order_discount +
            point_discount
        )
        
        # Bulatkan grand total ke ratusan
        grand_total = round(grand_total / 100) * 100
        
        # Validate point tidak melebihi total
        if abs(point_discount) > total_price_rounded:
            return CheckoutResponse(
                success=False,
                msg="Point tidak boleh melebihi total transaksi"
            )
        
        # Determine payment status
        if request.paying_method == 6:  # COD
            if request.paying_amount == 0:
                payment_status = "1"  # Belum bayar
            elif request.paying_amount < grand_total:
                payment_status = "3"  # Sebagian
            else:
                payment_status = "4"  # Lunas
        else:
            payment_status = "4"  # Lunas
        
        # Calculate paid amount
        paid_amount = grand_total if request.paying_amount >= grand_total else request.paying_amount
        change = request.paying_amount - grand_total
        
        # Validate payment untuk non-COD
        if request.is_dikirim == 0 and change < 0:
            return CheckoutResponse(
                success=False,
                msg=f"Pembayaran kurang: {abs(change)}"
            )
        
        # 4. Generate reference number
        reference_no = CheckoutService.generate_reference_no(transaksi.jenis_trx or 1)
        
        # 5. Begin transaction
        checkout_data = {
            'order_tax': request.order_tax,
            'order_tax_rate': request.order_tax_rate,
            'order_discount': order_discount,
            'shipping_cost': request.shipping_cost,
            'service_fee': request.service_fee,
            'point': point_discount,
            'paid_amount': paid_amount,
            'sale_note': request.sale_note,
            'staff_note': request.staff_note,
            'supervised': request.supervised,
            'customer_alias': request.customer_alias,
            'is_dikirim': request.is_dikirim
        }
        
        # 6. Create sale
        sale_id = await CheckoutService.create_sale(
            db=db,
            transaksi=transaksi,
            summary=summary,
            checkout_data=checkout_data,
            reference_no=reference_no,
            grand_total=grand_total,
            payment_status=payment_status,
            operator_id=current_user.id,
            store_id=current_user.store_id
        )
        
        # 7. Create product sales & update stock
        stock_updates = await CheckoutService.create_product_sales(
            db=db,
            transaksi_id=request.id_transaksi,
            reference_no=reference_no,
            store_id=current_user.store_id,
            warehouse_id=transaksi.warehouse_id
        )
        
        # 8. Create payment
        await CheckoutService.create_payment(
            db=db,
            reference_no=reference_no,
            payment_method_id=request.paying_method,
            paid_amount=paid_amount,
            paying_amount=request.paying_amount,
            payment_note=request.staff_note,
            operator_id=current_user.id,
            store_id=current_user.store_id
        )
        
        # 9. Create balance entries
        # Balance untuk penjualan
        await CheckoutService.create_balance_entry(
            db=db,
            jenis_id=1,  # 1 = Penjualan
            reference_no=reference_no,
            user_id=current_user.id,
            customer_id=transaksi.customer_id,
            jumlah=total_price_rounded,
            bayar=paid_amount,
            trx_id=sale_id,
            payment_method_id=request.paying_method,
            store_id=current_user.store_id,
            warehouse_id=transaksi.warehouse_id
        )
        
        # Balance untuk point (jika digunakan)
        if point_discount < 0:
            await CheckoutService.create_balance_entry(
                db=db,
                jenis_id=7,  # 7 = Bayar Point
                reference_no=reference_no,
                user_id=current_user.id,
                customer_id=transaksi.customer_id,
                jumlah=point_discount,
                bayar=0,
                trx_id=sale_id,
                payment_method_id=1,
                store_id=current_user.store_id,
                warehouse_id=transaksi.warehouse_id
            )
        
        # Balance untuk discount
        if order_discount < 0:
            await CheckoutService.create_balance_entry(
                db=db,
                jenis_id=9,  # 9 = Diskon Penjualan
                reference_no=reference_no,
                user_id=current_user.id,
                customer_id=transaksi.customer_id,
                jumlah=order_discount,
                bayar=0,
                trx_id=sale_id,
                payment_method_id=request.paying_method,
                store_id=current_user.store_id,
                warehouse_id=transaksi.warehouse_id
            )
        
        # Balance untuk shipping
        if request.shipping_cost > 0:
            await CheckoutService.create_balance_entry(
                db=db,
                jenis_id=10,  # 10 = Ongkir
                reference_no=reference_no,
                user_id=current_user.id,
                customer_id=transaksi.customer_id,
                jumlah=request.shipping_cost,
                bayar=0,
                trx_id=sale_id,
                payment_method_id=request.paying_method,
                store_id=current_user.store_id,
                warehouse_id=transaksi.warehouse_id
            )
        
        # Balance untuk service fee
        if request.service_fee > 0:
            await CheckoutService.create_balance_entry(
                db=db,
                jenis_id=11,  # 11 = Layanan
                reference_no=reference_no,
                user_id=current_user.id,
                customer_id=transaksi.customer_id,
                jumlah=request.service_fee,
                bayar=0,
                trx_id=sale_id,
                payment_method_id=request.paying_method,
                store_id=current_user.store_id,
                warehouse_id=transaksi.warehouse_id
            )
        
        # 10. Create customer log
        await CheckoutService.create_customer_log(
            db=db,
            customer_id=transaksi.customer_id,
            jenis_trx=1,  # 1 = Penjualan
            jumlah=grand_total,
            reff_id=sale_id,
            store_id=current_user.store_id,
            status_trx=1
        )
        
        # 11. Update transaksi status
        #transaksi.sale_status = '1'
        
        # 12. Delete transaksi & transaksi_detail (cart sudah jadi sale)
        querydt = text("""DELETE FROM transaksi_detail WHERE transaksi_id = :trans_id """)
        await db.execute(
            querydt,{
                "trans_id": request.id_transaksi
            }
        )
        queryT=text("""DELETE FROM transaksi WHERE id = :trans_id """)

        await db.execute(
        queryT,{
            "trans_id": request.id_transaksi
        }
        )
        
        # 13. Commit transaction
        await db.commit()
        
        return CheckoutResponse(
            success=True,
            msg="Transaksi berhasil",
            sale_id=sale_id,
            reference_no=reference_no,
            grand_total=grand_total,
            paying_amount=request.paying_amount,
            change=change if change > 0 else 0,
            piutang=abs(change) if change < 0 else 0
        )
        
    except Exception as e:
        await db.rollback()
        import traceback
        
        error_traceback = traceback.format_exc()
        error_lines = error_traceback.split('\n')
        
        error_location = "Unknown"
        for line in error_lines:
            if 'File "' in line and ('checkout' in line.lower() or 'transaksi' in line.lower()):
                error_location = line.strip()
                break
        
        print(f"\n❌ Error in finalize_transaction:")
        print(f"   Error: {str(e)}")
        print(f"   Location: {error_location}")
        if settings.DEBUG:
            print(f"\n{error_traceback}\n")
        
        return CheckoutResponse(
            success=False,
            msg=f"Error: {str(e)} | Location: {error_location}"
        )