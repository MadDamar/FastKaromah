<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Delivery extends Model
{
    use HasFactory;

    protected $fillable = [
        'sale_id', 'reference_sale', 'reference_no', 'address', 'to', 'delivered_by', 'recieved_by', 'file', 'note', 'status', 'sent_at', 'store_id'
    ];

    public function sale()
    {
        return $this->belongsTo(Sale::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}