<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ProductImage extends Model
{
    use HasFactory;

    public $timestamps = false;

    protected $fillable = [
        'url_image', 'url_thumb', 'url_local', 'store_id', 'product_category_id','image_id'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }

    public function Category()
    {
        return $this->belongsTo(Category::class);
    }
}