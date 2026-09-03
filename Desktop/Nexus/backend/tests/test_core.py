"""Tests for helpers, email, storage and background task modules."""

import asyncio
import io
import os
import sys
import types

from fastapi import UploadFile

from app.core import email as email_module
from app.core import storage
from app.tasks import email_tasks, notification_tasks
from app.utils import helpers


# --- helpers ---------------------------------------------------------------


def test_split_tags():
    assert helpers.split_tags(None) == []
    assert helpers.split_tags("") == []
    assert helpers.split_tags("a, b , c") == ["a", "b", "c"]


def test_now_utc():
    assert helpers.now_utc() is not None


# --- email -----------------------------------------------------------------


def test_send_email_no_key_returns_false():
    assert email_module.send_email("a@b.com", "s", "<p>hi</p>") is False
    assert email_module.send_verification_email("a@b.com", "tok") is False
    assert email_module.send_password_reset_email("a@b.com", "tok") is False


def test_send_email_success(monkeypatch):
    from app import config as config_mod

    monkeypatch.setattr(config_mod.settings, "resend_api_key", "fake-key")

    class FakeEmails:
        @staticmethod
        def send(*args, **kwargs):
            return {"id": "msg_1"}

    fake_resend = types.ModuleType("resend")
    fake_resend.api_key = None
    fake_resend.Emails = FakeEmails
    monkeypatch.setitem(sys.modules, "resend", fake_resend)

    assert email_module.send_email("a@b.com", "s", "<p>hi</p>") is True
    assert email_module.send_verification_email("a@b.com", "tok") is True
    assert email_module.send_password_reset_email("a@b.com", "tok") is True


# --- storage ----------------------------------------------------------------


def test_save_upload_no_filename():
    assert asyncio.run(storage.save_upload(UploadFile(filename="", file=io.BytesIO(b"")))) is None


def test_save_upload_local(monkeypatch):
    monkeypatch.setattr(storage.settings, "aws_access_key_id", "")
    monkeypatch.setattr(storage.settings, "aws_secret_access_key", "")
    file = UploadFile(filename="logo.png", file=io.BytesIO(b"binary"))
    url = asyncio.run(storage.save_upload(file))
    assert url == "/media/files/logo.png"
    assert os.path.exists("media/uploads/files/logo.png")
    os.remove("media/uploads/files/logo.png")


def test_save_upload_too_large():
    big = b"x" * (11 * 1024 * 1024)
    file = UploadFile(filename="big.png", file=io.BytesIO(big))
    try:
        asyncio.run(storage.save_upload(file))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_save_upload_s3(monkeypatch):
    monkeypatch.setattr(storage.settings, "aws_access_key_id", "key")
    monkeypatch.setattr(storage.settings, "aws_secret_access_key", "secret")
    monkeypatch.setattr(storage.settings, "aws_bucket_name", "my-bucket")
    monkeypatch.setattr(storage.settings, "aws_region", "us-east-1")

    class FakeS3Client:
        def put_object(self, **kwargs):
            return {}

    class FakeBoto3:
        def client(self, *args, **kwargs):
            return FakeS3Client()

    fake_boto3 = types.ModuleType("boto3")
    fake_boto3.client = lambda *a, **k: FakeS3Client()
    monkeypatch.setitem(sys.modules, "boto3", fake_boto3)

    file = UploadFile(filename="logo.png", file=io.BytesIO(b"data"))
    url = asyncio.run(storage.save_upload(file, folder="avatars"))
    assert url.startswith("https://my-bucket.s3.us-east-1.amazonaws.com/")


def test_save_upload_s3_fallback(monkeypatch):
    monkeypatch.setattr(storage.settings, "aws_access_key_id", "key")
    monkeypatch.setattr(storage.settings, "aws_secret_access_key", "secret")
    monkeypatch.setattr(storage.settings, "aws_bucket_name", "my-bucket")
    monkeypatch.setattr(storage.settings, "aws_region", "us-east-1")

    class FakeS3Client:
        def put_object(self, **kwargs):
            raise RuntimeError("boom")

    class FakeBoto3:
        def client(self, *args, **kwargs):
            return FakeS3Client()

    fake_boto3 = types.ModuleType("boto3")
    fake_boto3.client = lambda *a, **k: FakeS3Client()
    monkeypatch.setitem(sys.modules, "boto3", fake_boto3)

    file = UploadFile(filename="logo.png", file=io.BytesIO(b"data"))
    url = asyncio.run(storage.save_upload(file))
    # on S3 failure the local file remains the fallback
    assert url == "/media/files/logo.png"
    assert os.path.exists("media/uploads/files/logo.png")
    os.remove("media/uploads/files/logo.png")


# --- tasks -----------------------------------------------------------------


def test_email_tasks_return_bool():
    assert email_tasks.deliver_verification_email("a@b.com", "tok") is False
    assert email_tasks.deliver_password_reset_email("a@b.com", "tok") is False


def test_notification_task():
    assert notification_tasks.send_notification(1, "hello") is True
