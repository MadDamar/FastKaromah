<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Sale extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'user_id', 'customer_id', 'warehouse_id', 'biller_id', 'item', 'total_qty', 'total_discount', 'total_tax', 'total_price', 'grand_total', 'order_tax_rate', 'order_tax', 'order_discount', 'coupon_id', 'coupon_discount', 'shipping_cost', 'point_discount', 'service_fee', 'sale_status', 'payment_status', 'document', 'paid_amount', 'sale_note', 'staff_note', 'supervised', 'customer_alias', 'is_dikirim', 'status_kirim', 'is_deleted', 'store_id'
    ];

    public function productSale()
    {
        return $this->hasMany(ProductSale::class, 'reference_no');
    }
    public function payment()
    {
        return $this->hasOne(Payment::class, 'reference_no', 'reference_no');
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function biller()
    {
        return $this->belongsTo(Biller::class);
    }

    public function coupon()
    {
        return $this->belongsTo(Coupon::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}