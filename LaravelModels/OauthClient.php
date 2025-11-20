<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OauthClient extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id', 'name', 'secret', 'redirect', 'personal_access_client', 'password_client', 'revoked'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}