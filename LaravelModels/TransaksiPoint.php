<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TransaksiPoint extends Model
{
    use HasFactory;

    protected $fillable = [
        'sale_id', 'cust_id', 'jumlah', 'awal', 'akhir', 'store_id'
    ];

    public function sale()
    {
        return $this->belongsTo(Sale::class);
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class, 'cust_id');
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}