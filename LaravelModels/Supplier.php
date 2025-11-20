<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Supplier extends Model
{
    use HasFactory;

    protected $fillable = [
        'address', 'city', 'company_name', 'country', 'email', 'image', 'is_active', 'name', 'phone_number', 'postal_code', 'state', 'store_id', 'taxed', 'vat_number'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }

    public function products()
    {
        return $this->belongsToMany(Product::class, 'product_supplier');
    }
}
