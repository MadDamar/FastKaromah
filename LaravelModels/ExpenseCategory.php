<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ExpenseCategory extends Model
{
    use HasFactory;

    protected $fillable = [
        'code', 'name', 'is_active', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}