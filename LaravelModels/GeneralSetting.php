<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GeneralSetting extends Model
{
    use HasFactory;

    protected $fillable = [
        'site_title', 'site_logo', 'currency', 'staff_access', 'date_format', 'theme', 'store_id', 'currency_position'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}