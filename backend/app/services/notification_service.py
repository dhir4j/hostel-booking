import logging
from flask import current_app

logger = logging.getLogger(__name__)

def _send(subject: str, recipient: str, body: str) -> None:
    """Send email. Never raises — logs on failure."""
    try:
        from flask_mail import Message
        from app.extensions import mail
        msg = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(msg)
    except Exception as exc:
        logger.warning('Mail send failed to %s: %s', recipient, exc)

def send_password_reset(email: str, raw_token: str) -> None:
    frontend_url = current_app.config.get('FRONTEND_URL', '')
    link = f"{frontend_url}/reset-password/{raw_token}"
    _send(
        subject='Password Reset Request',
        recipient=email,
        body=f"Click to reset your password (expires in 30 min):\n{link}\n\nIgnore if you didn't request this.",
    )

def send_booking_submitted(email: str, booking_id: int) -> None:
    _send(
        subject='Booking Received',
        recipient=email,
        body=f"Your booking #{booking_id} has been submitted and is pending admin approval.",
    )

def send_booking_approved(email: str, booking_id: int) -> None:
    _send(
        subject='Booking Approved — Payment Required',
        recipient=email,
        body=f"Your booking #{booking_id} has been approved. Please complete payment to confirm.",
    )

def send_booking_rejected(email: str, booking_id: int, notes: str | None = None) -> None:
    body = f"Your booking #{booking_id} has been rejected."
    if notes:
        body += f"\nReason: {notes}"
    _send(subject='Booking Rejected', recipient=email, body=body)

def send_booking_cancelled(email: str, booking_id: int) -> None:
    _send(
        subject='Booking Cancelled',
        recipient=email,
        body=f"Your booking #{booking_id} has been cancelled.",
    )

def send_payment_confirmed(email: str, booking_id: int) -> None:
    _send(
        subject='Payment Confirmed — Booking Confirmed',
        recipient=email,
        body=f"Payment received. Your booking #{booking_id} is confirmed!",
    )
