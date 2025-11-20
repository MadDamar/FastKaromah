<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Quotation extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'user_id', 'biller_id', 'supplier_id', 'customer_id', 'warehouse_id', 'item', 'total_qty', 'total_discount', 'total_tax', 'total_price', 'order_tax_rate', 'order_tax', 'order_discount', 'shipping_cost', 'grand_total', 'quotation_status', 'document', 'note', 'store_id'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function biller()
    {
        return $this->belongsTo(Biller::class);
    }

    public function supplier()
    {
        return $this->belongsTo(Supplier::class);
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}