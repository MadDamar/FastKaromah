<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductLog extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'product_id', 'start_qty', 'end_qty', 'run_qty', 'status_qty', 'warehouse_id', 'store_id','created_at'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
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