<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TopedCat extends Model
{
    use HasFactory;

    protected $fillable = [
        'name', 'toped_cat_id'
    ];

    public function parent()
    {
        return $this->belongsTo(TopedCat::class, 'toped_cat_id');
    }
}
