<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PiutangDetail extends Model
{
    protected $table="hutang_detail";
    protected $fillable=["hutang_id","hutang_awal","hutang_akhir","keterangan"];
    public $timestamps = false;

    public function piutang(){
     return $this->belongsTo(Piutang::class,'hutang_id','hutang_id');
    }
}
