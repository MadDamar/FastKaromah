<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    use HasFactory;

    protected $fillable = [
        'name', 'description', 'guard_name', 'is_active', 'store_id'
    ];

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}