<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Purchase extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'faktur', 'user_id', 'warehouse_id', 'supplier_id', 'item', 'total_qty', 'total_discount', 'total_tax', 'total_cost', 'order_tax_rate', 'order_tax', 'order_discount', 'shipping_cost', 'grand_total', 'paid_amount', 'status', 'payment_status', 'document', 'note', 'due_date', 'store_id'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function supplier()
    {
        return $this->belongsTo(Supplier::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}