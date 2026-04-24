"""Testing configuration — fast, deterministic, rate-limit free."""

from __future__ import annotations

import os

from app.config.base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING: bool = True
    DEBUG: bool = False

    # Deterministic secrets; tests rely on these being stable across runs.
    SECRET_KEY: str = "test-secret-key"
    JWT_SECRET_KEY: str = "test-jwt-secret-key"

    # Shorter TTLs so freezegun-based expiry tests stay fast.
    JWT_ACCESS_TTL_MINUTES: int = 5
    JWT_REFRESH_TTL_DAYS: int = 1
    HOLD_TTL_MINUTES: int = 1
    PASSWORD_RESET_TTL_MINUTES: int = 5

    # Prefer TEST_DATABASE_URL when provided; fall back to DATABASE_URL.
    SQLALCHEMY_DATABASE_URI: str = (
        os.environ.get("TEST_DATABASE_URL")
        or os.environ.get("DATABASE_URL")
        or "postgresql://hostel:hostel@localhost:5432/hostel_test"
    )
    SQLALCHEMY_ECHO: bool = False

    # Disable rate limiting entirely so bursts from pytest don't 429.
    RATELIMIT_ENABLED: bool = False

    # Mail must never leave the test process.
    MAIL_SUPPRESS_SEND: bool = True

    WTF_CSRF_ENABLED: bool = False
    PAYMENT_PROVIDER: str = "mock"
    WEBHOOK_SECRET: str = "test-webhook-secret"
    INTERNAL_API_KEY: str = "test-internal-api-key"

    REFRESH_COOKIE_SECURE: bool = False
    REFRESH_COOKIE_SAMESITE: str = "Lax"

    @classmethod
    def validate(cls) -> None:  # pragma: no cover - deterministic in tests
        return None


__all__ = ["TestingConfig"]
