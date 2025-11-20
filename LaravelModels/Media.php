<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Media extends Model
{
    use HasFactory;

    protected $fillable = [
        'medially_type', 'medially_id', 'file_url', 'file_name', 'file_type', 'size', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}