<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    use HasFactory;

    protected $fillable = [
        'name', 'name_lbl', 'code', 'barcode', 'type', 'barcode_symbology', 'brand_id', 'category_id', 'unit_id', 'purchase_unit_id', 'sale_unit_id', 'cost', 'price', 'margin', 'qty', 'alert_quantity', 'promotion', 'promotion_price', 'max_item_promo', 'starting_date', 'last_date', 'tax_id', 'tax_method', 'image', 'file', 'is_variant', 'featured', 'product_list', 'qty_list', 'price_list', 'product_details', 'is_active', 'is_autoupdate', 'is_point', 'is_toped', 'is_shopee', 'last_adjustment', 'expired', 'store_id'
    ];

    public function productPrice(){
        return $this->hasMany(ProductPrice::class);
    }

    public function productWarehouse(){
        return $this->hasMany(ProductWarehouse::class);
    }

    public function brand()
    {
        return $this->belongsTo(Brand::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function unit()
    {
        return $this->belongsTo(Unit::class);
    }

    public function purchaseUnit()
    {
        return $this->belongsTo(Unit::class, 'purchase_unit_id');
    }

    public function saleUnit()
    {
        return $this->belongsTo(Unit::class, 'sale_unit_id');
    }

    public function tax()
    {
        return $this->belongsTo(Tax::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}
