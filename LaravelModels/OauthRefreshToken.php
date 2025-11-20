<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OauthRefreshToken extends Model
{
    use HasFactory;

    protected $fillable = [
        'access_token_id', 'revoked', 'expires_at'
    ];

    public function accessToken()
    {
        return $this->belongsTo(OauthAccessToken::class);
    }
}