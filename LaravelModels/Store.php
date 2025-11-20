<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Store extends Model
{
    use HasFactory;
    protected $table = 'store';

    protected $fillable = [
        'address', 'city_id', 'kecamatan_id', 'kelurahan_id', 'name', 'npwp', 'phone', 'province_id', 'slogan', 'store_logo', 'store_owner', 'store_type'
    ];

    public function categories()
    {
        return $this->hasMany(Category::class);
    }

    public function brands()
    {
        return $this->hasMany(Brand::class);
    }

    public function products()
    {
        return $this->hasMany(Product::class);
    }

    public function suppliers()
    {
        return $this->hasMany(Supplier::class);
    }

    public function city()
    {
        return $this->belongsTo(City::class);
    }

    public function kecamatan()
    {
        return $this->belongsTo(Kecamatan::class);
    }

    public function kelurahan()
    {
        return $this->belongsTo(Kelurahan::class);
    }

    public function province()
    {
        return $this->belongsTo(Province::class);
    }
}