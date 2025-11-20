<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Transaksi extends Model
{
    use HasFactory;
    protected $table = 'transaksi';

    protected $fillable = [
        'warehouse_id', 'biller_id', 'customer_id', 'sale_status', 'operator_id', 'tgl_transaksi', 'payment_method_id', 'jenis_trx', 'reference_sale', 'is_online'
    ];

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function biller()
    {
        return $this->belongsTo(Biller::class);
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }

    public function operator()
    {
        return $this->belongsTo(User::class, 'operator_id');
    }

    public function paymentMethod()
    {
        return $this->belongsTo(PaymentMethod::class);
    }
}