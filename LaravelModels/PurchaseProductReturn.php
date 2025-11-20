<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PurchaseProductReturn extends Model
{
    use HasFactory;

    protected $table = 'purchase_product_return';

    protected $fillable = [
        'return_id', 'reference_no', 'product_id', 'variant_id', 'qty', 'purchase_unit_id', 'net_unit_cost', 'discount', 'tax_rate', 'tax', 'total'
    ];

    public function return()
    {
        return $this->belongsTo(ReturnPurchase::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function variant()
    {
        return $this->belongsTo(Variant::class);
    }

    public function purchaseUnit()
    {
        return $this->belongsTo(Unit::class, 'purchase_unit_id');
    }
}