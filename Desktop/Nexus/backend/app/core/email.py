"""Email helpers. Uses Resend when configured, otherwise logs to console."""

import logging

from app.config import settings

logger = logging.getLogger("devhub.email")


def send_email(to_email: str, subject: str, html: str) -> bool:
    """Send an email via Resend when configured. Returns True on success."""
    if not settings.resend_api_key:
        logger.info("Email skipped (no RESEND_API_KEY). to=%s subject=%s", to_email, subject)
        return False

    import resend  # lazy import so the app starts without extra services

    resend.api_key = settings.resend_api_key
    try:
        resend.Emails.send({"from": "DevHub <noreply@devhub.app>", "to": [to_email], "subject": subject, "html": html})
        return True
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to send email to %s: %s", to_email, exc)
        return False


def send_verification_email(to_email: str, token: str) -> bool:
    link = f"{settings.frontend_url}/verify?token={token}"
    html = f"<p>برای تأیید ایمیل خود روی لینک زیر کلیک کنید.</p><p><a href='{link}'>{link}</a></p>"
    return send_email(to_email, "DevHub — تأیید ایمیل", html)


def send_password_reset_email(to_email: str, token: str) -> bool:
    link = f"{settings.frontend_url}/reset-password?token={token}"
    html = f"<p>برای بازیابی رمز عبور روی لینک زیر کلیک کنید.</p><p><a href='{link}'>{link}</a></p>"
    return send_email(to_email, "DevHub — بازیابی رمز عبور", html)
