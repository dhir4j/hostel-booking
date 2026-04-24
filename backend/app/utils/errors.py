"""Custom exception hierarchy and error code constants.

Every domain error raised by services/middleware inherits from :class:`AppError`
so the global error handler can render a consistent envelope
(``{success: false, error: {code, message, details}}``) with the correct HTTP
status code.

Error codes are UPPER_SNAKE constants; they are part of the public API surface
and must stay stable across versions.
"""

from __future__ import annotations

from typing import Any, Optional


# ---------------------------------------------------------------------------
# Error code constants (UPPER_SNAKE) — public API surface.
# ---------------------------------------------------------------------------

INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
UNAUTHORIZED = "UNAUTHORIZED"
FORBIDDEN = "FORBIDDEN"
NOT_FOUND = "NOT_FOUND"
VALIDATION_ERROR = "VALIDATION_ERROR"
INVALID_STATE_TRANSITION = "INVALID_STATE_TRANSITION"
CONFLICT = "CONFLICT"
ROOM_UNAVAILABLE = "ROOM_UNAVAILABLE"
HOLD_EXPIRED = "HOLD_EXPIRED"
PAYMENT_FAILED = "PAYMENT_FAILED"
RATE_LIMITED = "RATE_LIMITED"
INTERNAL_ERROR = "INTERNAL_ERROR"
BUSINESS_RULE = "BUSINESS_RULE"


# ---------------------------------------------------------------------------
# Base exception.
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Base class for all domain errors.

    Attributes:
        message: Human-readable message safe to expose to clients.
        code: UPPER_SNAKE error code string from the constants above.
        status_code: HTTP status used when rendering the response envelope.
        details: Optional structured diagnostics (field errors, hints, etc.).
    """

    message: str = "Application error"
    code: str = INTERNAL_ERROR
    status_code: int = 500

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message if message is not None else self.message
        self.code = code if code is not None else self.code
        self.status_code = (
            status_code if status_code is not None else self.status_code
        )
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Serialize to the ``error`` portion of the response envelope."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# 4xx hierarchy.
# ---------------------------------------------------------------------------

class ValidationError(AppError):
    message = "Validation failed"
    code = VALIDATION_ERROR
    status_code = 400


class AuthenticationError(AppError):
    message = "Authentication required"
    code = UNAUTHORIZED
    status_code = 401


class PermissionDeniedError(AppError):
    message = "You do not have permission to perform this action"
    code = FORBIDDEN
    status_code = 403


class NotFoundError(AppError):
    message = "Resource not found"
    code = NOT_FOUND
    status_code = 404


class ConflictError(AppError):
    message = "Conflicting state"
    code = CONFLICT
    status_code = 409


class InvalidStateTransitionError(AppError):
    message = "Invalid state transition"
    code = INVALID_STATE_TRANSITION
    status_code = 422


class BusinessRuleError(AppError):
    message = "Business rule violated"
    code = BUSINESS_RULE
    status_code = 422


class RoomUnavailableError(ConflictError):
    message = "Room is not available for the requested dates"
    code = ROOM_UNAVAILABLE
    status_code = 409


class PaymentError(AppError):
    message = "Payment failed"
    code = PAYMENT_FAILED
    status_code = 400


# ---------------------------------------------------------------------------
# 5xx hierarchy.
# ---------------------------------------------------------------------------

class ProviderError(AppError):
    """Upstream provider (payment gateway, mail server, etc.) failed."""

    message = "Upstream provider error"
    code = "PROVIDER_ERROR"
    status_code = 502


__all__ = [
    # constants
    "INVALID_CREDENTIALS",
    "UNAUTHORIZED",
    "FORBIDDEN",
    "NOT_FOUND",
    "VALIDATION_ERROR",
    "INVALID_STATE_TRANSITION",
    "CONFLICT",
    "ROOM_UNAVAILABLE",
    "HOLD_EXPIRED",
    "PAYMENT_FAILED",
    "RATE_LIMITED",
    "INTERNAL_ERROR",
    "BUSINESS_RULE",
    # exceptions
    "AppError",
    "ValidationError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "InvalidStateTransitionError",
    "BusinessRuleError",
    "RoomUnavailableError",
    "PaymentError",
    "ProviderError",
]
