<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DisposableWarehouse extends Model
{
    use HasFactory;

    protected $fillable = [
        'warehouse_id', 'disposable_id', 'qty'
    ];

    public function warehouse()
    {
        return $this->belongsTo(Warehouse::class);
    }

    public function disposable()
    {
        return $this->belongsTo(Disposable::class);
    }
}