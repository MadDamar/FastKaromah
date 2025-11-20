<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OnlineCart extends Model
{
    use HasFactory;

    protected $fillable = [
        'customer_id', 'product_id', 'barcode', 'name', 'qty', 'harga', 'total','store_id'
    ];

    public function store(){
        return $this->belongsTo(Store::class);
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }
}