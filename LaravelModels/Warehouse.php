<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Warehouse extends Model
{
    use HasFactory;

    protected $fillable = [
        'name', 'warehouse_code', 'phone', 'email', 'address', 'is_active', 'note','store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }

    public function product(){
        return $this->belongsTo(Product::class);
    }
}