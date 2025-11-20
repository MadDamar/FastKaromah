<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CouponLog extends Model
{
    use HasFactory;

    protected $fillable = [
        'coupon_id', 'reff_no'
    ];

    public function coupon()
    {
        return $this->belongsTo(Coupon::class);
    }

}