"""Email background tasks."""

from app.core.email import send_password_reset_email, send_verification_email


def deliver_verification_email(to_email: str, token: str) -> bool:
    return send_verification_email(to_email, token)


def deliver_password_reset_email(to_email: str, token: str) -> bool:
    return send_password_reset_email(to_email, token)
