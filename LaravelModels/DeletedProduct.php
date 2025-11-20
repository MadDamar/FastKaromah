<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DeletedProduct extends Model
{
    protected $table = 'deleted_products';

    protected $fillable = [
        'product_id',
        'productName',
        'qty',
        'price',
        'total',
        'jobs',
        'processed',
        'deleted_at',
        'store_id'
    ];

    public $timestamps = false;
}
