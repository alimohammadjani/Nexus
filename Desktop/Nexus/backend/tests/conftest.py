"""Pytest fixtures for the DevHub API."""

import os
from pathlib import Path

_path = Path(__file__).resolve().parent / "test_devhub.db"
if _path.exists():
    _path.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{_path}"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["SEED_DEMO"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

engine = create_engine("sqlite:///./test_devhub.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def _setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 201, response.text
    token = client.post(
        "/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
