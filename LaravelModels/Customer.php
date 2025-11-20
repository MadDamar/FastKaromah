<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Laravel\Sanctum\HasApiTokens;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Foundation\Auth\User as Authenticatable;

class Customer extends Authenticatable
{
    use HasFactory;
    use HasApiTokens;

    protected $fillable = [
        'kode_cust', 'customer_group_id', 'name', 'nik', 'tgl_lhr', 'company_name', 'email','password','google_id','token', 'phone_number', 'tax_no', 'address', 'kelurahan_id', 'kecamatan_id', 'city', 'state', 'postal_code', 'country', 'deposit', 'expense', 'is_active', 'point', 'latst_trx', 'piutang', 'max_piutang', 'laba_masuk', 'otp', 'store_id'
    ];
    protected $hidden = ["password","created_at","tax_no","otp","store_id"];

    public function customerGroup()
    {
        return $this->belongsTo(CustomerGroup::class);
    }

    public function kelurahan()
    {
        return $this->belongsTo(Kelurahan::class);
    }

    public function kecamatan()
    {
        return $this->belongsTo(Kecamatan::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}