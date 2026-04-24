"""Consistent JSON response envelope helpers.

All API handlers MUST return through :func:`success_response` or
:func:`error_response` so the client receives the canonical shape:

    {"success": bool, "data": any, "error": {...} | None, "meta": {}}
"""

from __future__ import annotations

from typing import Any, Optional, Tuple

from flask import Response, jsonify


def success_response(
    data: Any = None,
    meta: Optional[dict] = None,
    status: int = 200,
) -> Tuple[Response, int]:
    """Return a successful envelope.

    Args:
        data: Serializable payload; may be ``None`` for 204-style responses.
        meta: Pagination / contextual metadata. Always serialized as object.
        status: HTTP status code; defaults to 200.

    Returns:
        A ``(Response, status)`` tuple compatible with Flask view returns.
    """
    body = {
        "success": True,
        "data": data,
        "error": None,
        "meta": meta or {},
    }
    return jsonify(body), status


def error_response(
    code: str,
    message: str,
    details: Any = None,
    status: int = 400,
) -> Tuple[Response, int]:
    """Return an error envelope.

    Args:
        code: UPPER_SNAKE error code (see :mod:`app.utils.errors`).
        message: Human-readable, client-safe message.
        details: Optional structured diagnostics (field errors, hints).
        status: HTTP status code; defaults to 400.

    Returns:
        A ``(Response, status)`` tuple compatible with Flask view returns.
    """
    body = {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "meta": {},
    }
    return jsonify(body), status


__all__ = ["success_response", "error_response"]
