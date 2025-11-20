<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Pengguna extends Model
{
    use HasFactory;

    protected $fillable = [
        'store_id', 'name', 'email', 'password', 'remember_token', 'phone', 'company_name', 'role_id', 'biller_id', 'warehouse_id', 'is_active', 'is_deleted', 'auth_key'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }

    public function role()
    {
        return $this->belongsTo(Role::class);
    }

    public function biller()
    {
        return $this->belongsTo(Biller::class);
    }

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }
}