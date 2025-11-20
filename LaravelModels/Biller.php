<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Biller extends Model
{
    use HasFactory;

    protected $fillable = [
        'name', 'image', 'company_name', 'vat_number', 'email', 'phone_number', 'address', 'city', 'state', 'postal_code', 'country', 'is_active', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}