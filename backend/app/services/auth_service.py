"""Authentication service: register, login, token refresh, logout, password management."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone, timedelta

from flask import current_app
from sqlalchemy import select, update as sa_update

from app.extensions import db
from app.repositories import user_repo, audit_repo
from app.models.auth_token import AuthToken, PasswordReset
from app.utils.password import hash_password, verify_password
from app.utils.tokens import (
    encode_access_token,
    encode_refresh_token,
    hash_token,
    generate_reset_token,
)
from app.utils.errors import AuthenticationError, ValidationError


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _issue_refresh_token(
    user_id: int,
    user_agent: str | None,
    ip: str | None,
) -> tuple[str, str]:
    """Generate a refresh token, persist the hash, and return (raw, token_hash)."""
    raw = secrets.token_hex(32)
    token_hash = hash_token(raw)

    ttl_days = int(current_app.config.get("JWT_REFRESH_TTL_DAYS", 7))
    now = _now()
    expires_at = now + timedelta(days=ttl_days)

    auth_token = AuthToken(
        user_id=user_id,
        refresh_token_hash=token_hash,
        issued_at=now,
        expires_at=expires_at,
        user_agent=user_agent,
        ip=ip,
    )
    db.session.add(auth_token)
    db.session.flush()
    return raw, token_hash


def _revoke_all_refresh_tokens(user_id: int) -> None:
    """Revoke all active refresh tokens for a user."""
    now = _now()
    stmt = (
        sa_update(AuthToken)
        .where(AuthToken.user_id == user_id, AuthToken.revoked_at.is_(None))
        .values(revoked_at=now)
        .execution_options(synchronize_session="fetch")
    )
    db.session.execute(stmt)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def register_user(
    full_name: str,
    email: str,
    password: str,
    phone: str | None = None,
) -> object:
    """Register a new user account.

    Raises:
        ValidationError: If the email is already in use.
    """
    if user_repo.email_exists(email):
        raise ValidationError("An account with that email already exists.")

    password_hash = hash_password(password)
    user = user_repo.create(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
        phone=phone,
    )
    audit_repo.log(
        entity_type="user",
        entity_id=user.id,
        action="register",
        actor_user_id=user.id,
    )
    db.session.commit()
    return user


def login(
    email: str,
    password: str,
    user_agent: str | None = None,
    ip: str | None = None,
) -> tuple[str, str, object]:
    """Authenticate a user and issue tokens.

    Returns:
        (access_token, refresh_raw, user)

    Raises:
        AuthenticationError: On invalid credentials.
    """
    user = user_repo.get_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid email or password.")

    access_token = encode_access_token(user.id, user.role)
    refresh_raw, _ = _issue_refresh_token(user.id, user_agent, ip)

    audit_repo.log(
        entity_type="user",
        entity_id=user.id,
        action="login",
        actor_user_id=user.id,
        ip=ip,
    )
    db.session.commit()
    return access_token, refresh_raw, user


def refresh(
    refresh_token_raw: str,
    user_agent: str | None = None,
    ip: str | None = None,
) -> tuple[str, str]:
    """Rotate a refresh token and issue a new access token.

    Returns:
        (access_token, new_refresh_raw)

    Raises:
        AuthenticationError: If the token is invalid, revoked, or expired.
    """
    token_hash = hash_token(refresh_token_raw)
    stmt = select(AuthToken).where(AuthToken.refresh_token_hash == token_hash)
    auth_token = db.session.execute(stmt).scalar_one_or_none()

    if auth_token is None:
        raise AuthenticationError("Invalid refresh token.")
    if auth_token.revoked_at is not None:
        raise AuthenticationError("Refresh token has been revoked.")
    if auth_token.expires_at < _now():
        raise AuthenticationError("Refresh token has expired.")

    # Revoke old token
    auth_token.revoked_at = _now()
    db.session.flush()

    user = user_repo.get_by_id(auth_token.user_id)
    if user is None:
        raise AuthenticationError("User not found.")

    access_token = encode_access_token(user.id, user.role)
    new_refresh_raw, _ = _issue_refresh_token(user.id, user_agent, ip)

    db.session.commit()
    return access_token, new_refresh_raw


def logout(refresh_token_raw: str) -> None:
    """Revoke a refresh token.

    Raises:
        AuthenticationError: If the token is not found.
    """
    token_hash = hash_token(refresh_token_raw)
    stmt = select(AuthToken).where(AuthToken.refresh_token_hash == token_hash)
    auth_token = db.session.execute(stmt).scalar_one_or_none()

    if auth_token is None:
        raise AuthenticationError("Invalid refresh token.")

    auth_token.revoked_at = _now()
    db.session.commit()


def forgot_password(email: str) -> None:
    """Initiate a password reset flow.

    Always returns None — never reveals whether the email exists.
    """
    from app.services import notification_service

    user = user_repo.get_by_email(email)
    if user is None:
        return

    raw_token, token_hash = generate_reset_token()

    ttl_minutes = int(current_app.config.get("PASSWORD_RESET_TTL_MINUTES", 30))
    expires_at = _now() + timedelta(minutes=ttl_minutes)

    reset = PasswordReset(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.session.add(reset)
    db.session.commit()

    notification_service.send_password_reset(user.email, raw_token)


def reset_password(raw_token: str, new_password: str) -> None:
    """Complete a password reset using a raw reset token.

    Raises:
        AuthenticationError: If the token is invalid, expired, or already used.
    """
    token_hash = hash_token(raw_token)
    stmt = select(PasswordReset).where(PasswordReset.token_hash == token_hash)
    reset = db.session.execute(stmt).scalar_one_or_none()

    if reset is None:
        raise AuthenticationError("Invalid or expired password reset token.")
    if reset.used_at is not None:
        raise AuthenticationError("Password reset token has already been used.")
    if reset.expires_at < _now():
        raise AuthenticationError("Password reset token has expired.")

    user = user_repo.get_by_id(reset.user_id)
    if user is None:
        raise AuthenticationError("User not found.")

    user.password_hash = hash_password(new_password)
    reset.used_at = _now()

    _revoke_all_refresh_tokens(user.id)

    db.session.commit()


def change_password(
    user_id: int,
    current_password: str,
    new_password: str,
) -> None:
    """Change a user's password after verifying the current one.

    Raises:
        AuthenticationError: If the current password is incorrect.
    """
    user = user_repo.get_by_id(user_id)
    if user is None or not verify_password(current_password, user.password_hash):
        raise AuthenticationError("Current password is incorrect.")

    user.password_hash = hash_password(new_password)
    _revoke_all_refresh_tokens(user_id)

    db.session.commit()
