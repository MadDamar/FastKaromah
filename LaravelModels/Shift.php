<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Shift extends Model
{
    use HasFactory;

    protected $fillable = [
        'shiftname', 'start_time', 'end_time', 'start_break', 'end_break', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}