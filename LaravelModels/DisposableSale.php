<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DisposableSale extends Model
{
    use HasFactory;

    protected $fillable = [
        'store_id', 'warehouse_id', 'reference_no', 'product_id', 'disposable_id', 'running_qty', 'start_qty', 'end_qty', 'trx_type'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function disposable()
    {
        return $this->belongsTo(Disposable::class);
    }
}