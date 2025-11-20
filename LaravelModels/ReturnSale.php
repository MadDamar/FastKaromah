<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ReturnSale extends Model
{
    use HasFactory;
    protected $table="return";

    protected $fillable = [
        'reference_no', 'reference_sale', 'user_id', 'customer_id', 'warehouse_id', 'biller_id', 'account_id', 'supervised', 'item', 'total_qty', 'total_discount', 'total_tax', 'total_price', 'order_tax_rate', 'order_tax', 'grand_total', 'service_fee', 'shipping_cost', 'coupon_discount', 'order_discount', 'coupon_id', 'document', 'return_note', 'staff_note', 'store_id'
    ];

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

    public function account()
    {
        return $this->belongsTo(Account::class);
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