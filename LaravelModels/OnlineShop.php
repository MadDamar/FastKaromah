<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OnlineShop extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}
