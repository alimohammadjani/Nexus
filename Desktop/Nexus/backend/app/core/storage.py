"""Storage helpers. Defaults to local disk; S3 when configured."""

from pathlib import Path

from fastapi import UploadFile

from app.config import settings

UPLOAD_ROOT = Path("media") / "uploads"
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


async def save_upload(file: UploadFile, folder: str = "files") -> str | None:
    """Persist an upload and return a publicly reachable URL or relative path."""
    if not file.filename:
        return None
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    target_dir = UPLOAD_ROOT / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    target = target_dir / safe_name

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("File exceeds maximum allowed size.")

    target.write_bytes(content)

    if settings.aws_access_key_id and settings.aws_secret_access_key:
        # Best-effort S3/R2 upload; local file remains as fallback.
        try:
            import boto3

            client = boto3.client(
                "s3",
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
            )
            client.put_object(
                Bucket=settings.aws_bucket_name,
                Key=f"{folder}/{safe_name}",
                Body=content,
                ContentType=file.content_type or "application/octet-stream",
            )
            return f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{folder}/{safe_name}"
        except Exception:
            pass

    return f"/media/{folder}/{safe_name}"
