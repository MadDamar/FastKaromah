<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductAdjustment extends Model
{
    use HasFactory;

    protected $fillable = [
        'adjustment_id', 'product_id', 'qty', 'action'
    ];

    public function adjustment()
    {
        return $this->belongsTo(Adjustment::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }
}