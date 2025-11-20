<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Account extends Model
{
    use HasFactory;

    protected $fillable = [
        'account_no', 'name', 'initial_balance', 'total_balance', 'note', 'is_default', 'is_active', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}