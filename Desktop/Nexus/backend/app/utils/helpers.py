"""Small helpers shared across the backend."""

from datetime import datetime


def now_utc() -> datetime:
    return datetime.utcnow()


def split_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [tag.strip() for tag in raw.split(",") if tag.strip()]
