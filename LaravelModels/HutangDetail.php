<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class HutangDetail extends Model
{
    use HasFactory;

    protected $fillable = [
        'hutang_id', 'hutang_awal', 'hutang_akhir', 'hutang_kembali', 'keterangan'
    ];

    public function hutang()
    {
        return $this->belongsTo(Hutang::class);
    }
}
