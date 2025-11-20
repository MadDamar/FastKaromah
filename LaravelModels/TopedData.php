<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TopedData extends Model
{
    use HasFactory;

    protected $fillable = [
        'product_id', 'barcode', 'name', 'weight', 'weight_unit', 'etalase_id', 'category_id', 'up_price', 'min_order', 'stock_updated', 'price_updated', 'description', 'autoupdate'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}