<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RegionGroup extends Model
{
    use HasFactory;

    protected $fillable = [
        'region_id', 'kelurahan_id'
    ];

    public function region()
    {
        return $this->belongsTo(Region::class);
    }

    public function kelurahan()
    {
        return $this->belongsTo(Kelurahan::class);
    }
}