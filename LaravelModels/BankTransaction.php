<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class BankTransaction extends Model
{
    use HasFactory;

    protected $fillable = [
        'reference_no', 'account_id', 'amount', 'transaction_type', 'store_id'
    ];

    public function account()
    {
        return $this->belongsTo(Account::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}