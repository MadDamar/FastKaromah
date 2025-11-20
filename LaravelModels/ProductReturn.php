<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductReturn extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'product_id', 'variant_id', 'qty', 'sale_unit_id', 'net_unit_price', 'discount', 'tax_rate', 'tax', 'total'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function variant()
    {
        return $this->belongsTo(Variant::class);
    }

    public function saleUnit()
    {
        return $this->belongsTo(Unit::class, 'sale_unit_id');
    }
}