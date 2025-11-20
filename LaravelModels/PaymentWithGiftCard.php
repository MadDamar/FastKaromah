<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PaymentWithGiftCard extends Model
{
    use HasFactory;

    protected $fillable = [
        'payment_id', 'gift_card_id'
    ];

    public function payment()
    {
        return $this->belongsTo(Payment::class);
    }

    public function giftCard()
    {
        return $this->belongsTo(GiftCard::class);
    }
}