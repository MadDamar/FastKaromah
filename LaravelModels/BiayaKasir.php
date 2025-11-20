<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class BiayaKasir extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id', 'reff_no', 'jumlah', 'keterangan'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}