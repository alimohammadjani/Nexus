"""Auth endpoint tests."""


def test_register_and_login(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "test@example.com"

    login = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert login.status_code == 200
    assert login.json()["access_token"]


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "full_name": "Test User", "password": "password123"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_duplicate_email(client):
    payload = {"email": "test@example.com", "full_name": "Test User", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_me(client, auth_headers):
    resp = client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"
