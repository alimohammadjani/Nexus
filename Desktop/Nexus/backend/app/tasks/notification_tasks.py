"""Notification background helpers (stubbed for Celery/Redis integration)."""

import logging

logger = logging.getLogger("devhub.notifications")


def send_notification(user_id: int, message: str) -> bool:
    """Enqueue/consume a notification. Currently logs to console."""
    logger.info("Notification for user %s: %s", user_id, message)
    return True
