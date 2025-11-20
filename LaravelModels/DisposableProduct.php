<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DisposableProduct extends Model
{
    use HasFactory;

    protected $fillable = [
        'product_id', 'disposable_id', 'running_qty'
    ];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function disposable()
    {
        return $this->belongsTo(Disposable::class);
    }
}