<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Payment extends Model
{
    use HasFactory;

    protected $fillable = [
        'payment_reference', 'user_id', 'purchase_id', 'sale_id', 'reference_no', 'account_id', 'paying', 'amount', 'change', 'paying_method', 'payment_note', 'store_id'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function purchase()
    {
        return $this->belongsTo(Purchase::class);
    }

    public function sale()
    {
        return $this->belongsTo(Sale::class, 'reference_no', 'reference_no');
    }

    public function account()
    {
        return $this->belongsTo(Account::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}