"""Date parsing, validation, and interval arithmetic helpers."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Union

from app.utils.errors import ValidationError

MAX_BOOKING_SPAN_DAYS = 90


def parse_iso_date(s: Union[str, date, datetime]) -> date:
    """Parse an ISO-8601 date string (``YYYY-MM-DD``) into a :class:`date`.

    Accepts already-parsed :class:`date` / :class:`datetime` objects for
    convenience; datetimes are converted to their ``.date()`` component.
    """
    if isinstance(s, datetime):
        return s.date()
    if isinstance(s, date):
        return s
    if not isinstance(s, str) or not s:
        raise ValidationError(
            message="Expected ISO-8601 date (YYYY-MM-DD)",
            details={"value": s},
        )
    try:
        return date.fromisoformat(s)
    except ValueError as exc:
        raise ValidationError(
            message="Invalid ISO-8601 date",
            details={"value": s, "reason": str(exc)},
        ) from exc


def _today_utc() -> date:
    return datetime.now(timezone.utc).date()


def validate_booking_dates(check_in: date, check_out: date) -> None:
    """Enforce the booking-date business rules.

    Rules:
        * ``check_in`` must be today or future (UTC).
        * ``check_out`` must be strictly after ``check_in``.
        * Span (``check_out - check_in``) must be at most
          :data:`MAX_BOOKING_SPAN_DAYS` days.

    Raises:
        ValidationError: On any rule violation. The ``details`` dict identifies
            the failing field(s).
    """
    if not isinstance(check_in, date) or not isinstance(check_out, date):
        raise ValidationError(
            message="check_in and check_out must be dates",
            details={"check_in": check_in, "check_out": check_out},
        )

    today = _today_utc()
    if check_in < today:
        raise ValidationError(
            message="check_in must be today or a future date",
            details={"check_in": check_in.isoformat(), "today": today.isoformat()},
        )

    if check_out <= check_in:
        raise ValidationError(
            message="check_out must be strictly after check_in",
            details={
                "check_in": check_in.isoformat(),
                "check_out": check_out.isoformat(),
            },
        )

    span_days = (check_out - check_in).days
    if span_days > MAX_BOOKING_SPAN_DAYS:
        raise ValidationError(
            message=(
                f"Booking span must be at most {MAX_BOOKING_SPAN_DAYS} days"
            ),
            details={
                "span_days": span_days,
                "max_span_days": MAX_BOOKING_SPAN_DAYS,
            },
        )


def ranges_overlap(
    a_start: date,
    a_end: date,
    b_start: date,
    b_end: date,
) -> bool:
    """Return ``True`` if half-open intervals ``[a_start, a_end)`` and
    ``[b_start, b_end)`` overlap.

    Touching intervals (``a_end == b_start``) do NOT overlap under the
    half-open convention — this is the convention the overlap SQL predicate
    uses (``a.start < b.end AND a.end > b.start``).
    """
    return a_start < b_end and a_end > b_start


__all__ = [
    "MAX_BOOKING_SPAN_DAYS",
    "parse_iso_date",
    "validate_booking_dates",
    "ranges_overlap",
]
