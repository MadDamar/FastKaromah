<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TransaksiDetail extends Model
{
    use HasFactory;

    protected $fillable = [
        'transaksi_id', 'barcode', 'product_id', 'nama', 'jumlah', 'unit', 'harga', 'total', 'diskon', 'profit', 'is_point', 'tax_rate', 'tax', 'unit_id'
    ];

    public function transaksi()
    {
        return $this->belongsTo(Transaksi::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function unit()
    {
        return $this->belongsTo(Unit::class);
    }
}