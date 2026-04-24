"""Base configuration loaded from environment variables.

Every env-driven setting lives here so subclasses only need to override the
handful that differ per environment. Secrets default to ``None`` so production
validation can detect missing values; non-secret knobs get safe defaults.
"""

from __future__ import annotations

import os
from typing import List, Optional


def _as_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "y", "t"}


def _as_int(value: Optional[str], default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _split_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def _normalize_db_url(url: Optional[str]) -> Optional[str]:
    """Rewrite Heroku-style ``postgres://`` to ``postgresql://``.

    SQLAlchemy 2.x rejects the legacy scheme; we fix it once centrally.
    """
    if not url:
        return url
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://") :]
    return url


class BaseConfig:
    """Shared configuration. Subclass for per-environment overrides."""

    # ---- Runtime ---------------------------------------------------------
    APP_ENV: str = os.environ.get("APP_ENV", "development")
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")
    TESTING: bool = False
    DEBUG: bool = False
    PROPAGATE_EXCEPTIONS: bool = True

    # ---- Database --------------------------------------------------------
    SQLALCHEMY_DATABASE_URI: Optional[str] = _normalize_db_url(
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = _as_bool(os.environ.get("SQLALCHEMY_ECHO"), False)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }

    # ---- JWT -------------------------------------------------------------
    JWT_SECRET_KEY: Optional[str] = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TTL_MINUTES: int = _as_int(
        os.environ.get("JWT_ACCESS_TTL_MINUTES"), 15
    )
    JWT_REFRESH_TTL_DAYS: int = _as_int(
        os.environ.get("JWT_REFRESH_TTL_DAYS"), 7
    )

    # ---- CORS ------------------------------------------------------------
    FRONTEND_URL: str = os.environ.get(
        "FRONTEND_URL", "http://localhost:3000"
    )
    CORS_ORIGINS: List[str] = _split_csv(
        os.environ.get("CORS_ORIGINS", "http://localhost:3000")
    )

    # ---- Rate Limiting ---------------------------------------------------
    RATELIMIT_STORAGE_URI: str = os.environ.get(
        "RATELIMIT_STORAGE_URI", "memory://"
    )
    RATELIMIT_ENABLED: bool = _as_bool(
        os.environ.get("RATELIMIT_ENABLED"), True
    )
    RATELIMIT_HEADERS_ENABLED: bool = True
    RATELIMIT_DEFAULT: Optional[str] = os.environ.get("RATELIMIT_DEFAULT")

    # ---- Payments --------------------------------------------------------
    PAYMENT_PROVIDER: str = os.environ.get("PAYMENT_PROVIDER", "mock")
    WEBHOOK_SECRET: Optional[str] = os.environ.get("WEBHOOK_SECRET")
    STRIPE_SECRET_KEY: Optional[str] = os.environ.get("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.environ.get(
        "STRIPE_WEBHOOK_SECRET"
    )
    RAZORPAY_KEY_ID: Optional[str] = os.environ.get("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: Optional[str] = os.environ.get("RAZORPAY_KEY_SECRET")
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = os.environ.get(
        "RAZORPAY_WEBHOOK_SECRET"
    )

    # ---- Mail ------------------------------------------------------------
    MAIL_SERVER: Optional[str] = os.environ.get("MAIL_SERVER")
    MAIL_PORT: int = _as_int(os.environ.get("MAIL_PORT"), 587)
    MAIL_USERNAME: Optional[str] = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS: bool = _as_bool(os.environ.get("MAIL_USE_TLS"), True)
    MAIL_USE_SSL: bool = _as_bool(os.environ.get("MAIL_USE_SSL"), False)
    MAIL_DEFAULT_SENDER: str = os.environ.get(
        "MAIL_FROM", "no-reply@hostel.app"
    )
    MAIL_SUPPRESS_SEND: bool = _as_bool(
        os.environ.get("MAIL_SUPPRESS_SEND"), False
    )

    # ---- Business Rules --------------------------------------------------
    HOLD_TTL_MINUTES: int = _as_int(
        os.environ.get("HOLD_TTL_MINUTES"), 30
    )
    PASSWORD_RESET_TTL_MINUTES: int = _as_int(
        os.environ.get("PASSWORD_RESET_TTL_MINUTES"), 30
    )
    PASSWORD_MIN_LENGTH: int = _as_int(
        os.environ.get("PASSWORD_MIN_LENGTH"), 8
    )

    # ---- Logging ---------------------------------------------------------
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()

    # ---- Internal --------------------------------------------------------
    INTERNAL_API_KEY: Optional[str] = os.environ.get("INTERNAL_API_KEY")

    # ---- Session / Cookies ----------------------------------------------
    # The refresh-token cookie flags. Subclasses tighten these in prod.
    REFRESH_COOKIE_NAME: str = "refresh_token"
    REFRESH_COOKIE_PATH: str = "/api/v1/auth"
    REFRESH_COOKIE_HTTPONLY: bool = True
    REFRESH_COOKIE_SECURE: bool = False
    REFRESH_COOKIE_SAMESITE: str = "Lax"

    # ---- Misc -----------------------------------------------------------
    JSON_SORT_KEYS: bool = False
    MAX_CONTENT_LENGTH: int = 2 * 1024 * 1024  # 2 MB request body cap

    @classmethod
    def validate(cls) -> None:
        """Raise ``RuntimeError`` if required secrets are unset.

        Called by the app factory before extensions are initialized so we
        fail fast with a clear message instead of a cryptic DB / JWT error.
        """
        missing: list[str] = []
        if not cls.SECRET_KEY:
            missing.append("SECRET_KEY")
        if not cls.JWT_SECRET_KEY:
            missing.append("JWT_SECRET_KEY")
        if not cls.SQLALCHEMY_DATABASE_URI:
            missing.append("DATABASE_URL")
        if missing:
            raise RuntimeError(
                "Missing required configuration: " + ", ".join(missing)
            )


__all__ = ["BaseConfig"]
