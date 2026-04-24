"""Development configuration — forgiving defaults for local boot."""

from __future__ import annotations

import os

from app.config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = False

    # Helpful local defaults so the app still boots without a full .env.
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"
    JWT_SECRET_KEY: str = (
        os.environ.get("JWT_SECRET_KEY") or "dev-jwt-secret-change-me"
    )
    SQLALCHEMY_DATABASE_URI: str = (
        BaseConfig.SQLALCHEMY_DATABASE_URI
        or "postgresql://hostel:hostel@localhost:5432/hostel_dev"
    )

    SQLALCHEMY_ECHO: bool = (
        os.environ.get("SQLALCHEMY_ECHO", "").strip().lower()
        in {"1", "true", "yes", "on"}
    )

    # Cookies over http://localhost.
    REFRESH_COOKIE_SECURE: bool = False
    REFRESH_COOKIE_SAMESITE: str = "Lax"

    @classmethod
    def validate(cls) -> None:  # pragma: no cover - permissive in dev
        # Development mode never raises; we accept fallback defaults.
        return None


__all__ = ["DevelopmentConfig"]
