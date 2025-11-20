<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PosSetting extends Model
{
    use HasFactory;

    protected $fillable = [
        'customer_id', 'warehouse_id', 'biller_id', 'product_number', 'keybord_active', 'stripe_public_key', 'stripe_secret_key'
    ];

    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function biller()
    {
        return $this->belongsTo(Biller::class);
    }
}