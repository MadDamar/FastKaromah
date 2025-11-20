<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ReturnPurchase extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'supplier_id', 'warehouse_id', 'user_id', 'account_id', 'item', 'total_qty', 'total_discount', 'total_tax', 'total_cost', 'order_tax_rate', 'order_tax', 'grand_total', 'document', 'return_note', 'status_return', 'staff_note', 'store_id'
    ];

    public function supplier()
    {
        return $this->belongsTo(Supplier::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function account()
    {
        return $this->belongsTo(Account::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}