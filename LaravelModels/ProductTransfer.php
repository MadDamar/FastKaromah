<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductTransfer extends Model
{
    use HasFactory;
    protected $table = 'product_transfer';

    protected $fillable = [
        'reference_no', 'product_id', 'variant_id', 'qty', 'purchase_unit_id', 'net_unit_cost', 'tax_rate', 'tax', 'total'
    ];

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