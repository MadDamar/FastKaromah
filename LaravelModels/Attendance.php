<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Attendance extends Model
{
    use HasFactory;

    protected $fillable = [
        'date', 'employee_id', 'clock_in', 'clock_out', 'start_break', 'end_break', 'status', 'break_status', 'shift_id', 'note', 'fingerprint_data', 'store_id'
    ];

    public function employee()
    {
        return $this->belongsTo(Employee::class);
    }

    public function shift()
    {
        return $this->belongsTo(Shift::class);
    }

    public function store()
    {
        return $this->belongsTo(Store::class);
    }
}