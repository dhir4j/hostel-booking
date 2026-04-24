"""JWT and opaque-token helpers.

* Access tokens: HS256, short-lived, carry ``sub`` (stringified user id),
  ``role``, ``type=access``, ``jti``.
* Refresh tokens: HS256, long-lived, carry ``sub`` (stringified user id),
  ``type=refresh``, ``jti``. The raw token is returned once to the caller and
  stored server-side as ``sha256(raw)`` in ``auth_tokens``.
* Password reset tokens: opaque 32-byte hex; only the sha256 hash is stored.

PyJWT >= 2.10 enforces that ``sub`` be a string; we always cast ``user_id``.
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Tuple

import jwt
from flask import current_app

ALGORITHM = "HS256"
TYPE_ACCESS = "access"
TYPE_REFRESH = "refresh"


# ---------------------------------------------------------------------------
# Internal helpers.
# ---------------------------------------------------------------------------

def _secret() -> str:
    key = current_app.config.get("JWT_SECRET_KEY")
    if not key:
        raise RuntimeError("JWT_SECRET_KEY is not configured")
    return key


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_jti() -> str:
    return uuid.uuid4().hex


# ---------------------------------------------------------------------------
# JWT encode / decode.
# ---------------------------------------------------------------------------

def encode_access_token(
    user_id: int,
    role: str,
    jti: Optional[str] = None,
) -> str:
    """Encode a short-lived access JWT.

    Args:
        user_id: Integer primary key; stored as string in ``sub`` per RFC 7519.
        role: The user's role string (``"user"`` or ``"admin"``).
        jti: Optional explicit jti; one is generated if omitted.

    Returns:
        The encoded JWT string.
    """
    ttl_minutes = int(current_app.config.get("JWT_ACCESS_TTL_MINUTES", 15))
    now = _now()
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": TYPE_ACCESS,
        "iat": now,
        "exp": now + timedelta(minutes=ttl_minutes),
        "jti": jti or _new_jti(),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def encode_refresh_token(
    user_id: int,
    jti: Optional[str] = None,
) -> str:
    """Encode a long-lived refresh JWT."""
    ttl_days = int(current_app.config.get("JWT_REFRESH_TTL_DAYS", 7))
    now = _now()
    payload = {
        "sub": str(user_id),
        "type": TYPE_REFRESH,
        "iat": now,
        "exp": now + timedelta(days=ttl_days),
        "jti": jti or _new_jti(),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def decode_token(
    token: str,
    expected_type: Optional[str] = None,
) -> dict[str, Any]:
    """Decode + verify a JWT, enforcing ``type`` if provided.

    Raises:
        jwt.InvalidTokenError: Signature bad, expired, malformed, or wrong
            ``type``. Callers should map to ``AuthenticationError``.
    """
    try:
        payload = jwt.decode(token, _secret(), algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise
    if expected_type is not None and payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(
            f"expected token type {expected_type!r}, got {payload.get('type')!r}"
        )
    return payload


# ---------------------------------------------------------------------------
# Opaque token helpers (password reset + refresh-token hashing).
# ---------------------------------------------------------------------------

def hash_token(raw: str) -> str:
    """Return the hex ``sha256`` digest of ``raw``.

    Used for both password-reset lookup and refresh-token storage so the DB
    never contains a token that could be replayed if leaked.
    """
    if not isinstance(raw, str) or not raw:
        raise ValueError("token must be a non-empty string")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def generate_reset_token() -> Tuple[str, str]:
    """Generate a password-reset token.

    Returns:
        ``(raw_hex, sha256_hex)``. Email the raw value; persist the hash.
    """
    raw = secrets.token_hex(32)
    return raw, hash_token(raw)


__all__ = [
    "ALGORITHM",
    "TYPE_ACCESS",
    "TYPE_REFRESH",
    "encode_access_token",
    "encode_refresh_token",
    "decode_token",
    "hash_token",
    "generate_reset_token",
]
