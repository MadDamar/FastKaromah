<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PaymentWithCheque extends Model
{
    use HasFactory;

    protected $fillable = [
        'payment_id', 'cheque_no'
    ];

    public function payment()
    {
        return $this->belongsTo(Payment::class);
    }
}
