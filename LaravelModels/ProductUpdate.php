<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductUpdate extends Model
{
    use HasFactory;

    protected $fillable = [
        'barcode', 'product_id'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }
}