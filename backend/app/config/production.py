"""Production configuration — strict validation, secure cookies, HTTPS."""

from __future__ import annotations

from app.config.base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    TESTING: bool = False

    # Ensure error handlers run even when hosted behind Flask's default
    # exception propagation (PythonAnywhere / gunicorn).
    PROPAGATE_EXCEPTIONS: bool = True

    # Secure cookies require HTTPS. The refresh-token cookie is cross-site
    # from the frontend, so we use SameSite=None + Secure.
    REFRESH_COOKIE_SECURE: bool = True
    REFRESH_COOKIE_SAMESITE: str = "None"

    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"

    # Chatty echo is catastrophic in prod.
    SQLALCHEMY_ECHO: bool = False

    @classmethod
    def validate(cls) -> None:
        super().validate()
        missing: list[str] = []
        if not cls.INTERNAL_API_KEY:
            missing.append("INTERNAL_API_KEY")
        if cls.PAYMENT_PROVIDER == "mock":
            # Not fatal, but surface via warning-style message in production.
            missing.append("PAYMENT_PROVIDER (mock is not allowed in production)")
        if cls.PAYMENT_PROVIDER == "stripe" and not cls.STRIPE_SECRET_KEY:
            missing.append("STRIPE_SECRET_KEY")
        if cls.PAYMENT_PROVIDER == "razorpay" and not cls.RAZORPAY_KEY_SECRET:
            missing.append("RAZORPAY_KEY_SECRET")
        if missing:
            raise RuntimeError(
                "Production configuration invalid: " + ", ".join(missing)
            )


__all__ = ["ProductionConfig"]
