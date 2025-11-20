<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Disposable extends Model
{
    use HasFactory;

    protected $fillable = [
        'store_id', 'name'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}