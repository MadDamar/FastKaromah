<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Piutang extends Model
{
    protected $table="hutang";
    protected $primaryKey="hutang_id";
    protected $fillable =["ref_no","jumlah","customers_id","user_id","store_id"];
}
