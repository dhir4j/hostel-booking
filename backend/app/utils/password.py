"""Password hashing utilities backed by passlib[bcrypt].

We pin ``bcrypt<4.1`` in ``requirements.txt`` to avoid the known
``AttributeError: module 'bcrypt' has no attribute '__about__'`` bug that
breaks passlib 1.7.4 on bcrypt >= 4.1.
"""

from __future__ import annotations

from passlib.hash import bcrypt

_BCRYPT_ROUNDS = 12
_HASHER = bcrypt.using(rounds=_BCRYPT_ROUNDS)


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of ``plain`` using cost ``12``.

    Args:
        plain: The raw password. Must be a non-empty string.

    Returns:
        The bcrypt hash string, safe to store in the database.

    Raises:
        ValueError: If ``plain`` is empty.
    """
    if not isinstance(plain, str) or not plain:
        raise ValueError("password must be a non-empty string")
    return _HASHER.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time verification of ``plain`` against ``hashed``.

    Returns ``False`` (never raises) on malformed/empty inputs so callers can
    treat the outcome as a simple boolean without try/except noise.
    """
    if not isinstance(plain, str) or not plain:
        return False
    if not isinstance(hashed, str) or not hashed:
        return False
    try:
        return bcrypt.verify(plain, hashed)
    except (ValueError, TypeError):
        return False


__all__ = ["hash_password", "verify_password"]
