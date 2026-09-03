"""User endpoint tests."""


def test_list_users(client):
    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_users_search(client, auth_headers):
    resp = client.get("/api/v1/users?search=test")
    assert resp.status_code == 200
    assert any(u["email"] == "test@example.com" for u in resp.json())


def test_my_profile(client, auth_headers):
    resp = client.get("/api/v1/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


def test_get_user_and_404(client, auth_headers):
    resp = client.get("/api/v1/users/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1
    assert client.get("/api/v1/users/99999").status_code == 404


def test_update_me_full_name(client, auth_headers):
    resp = client.put("/api/v1/users/me", json={"full_name": "Updated Name"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Updated Name"


def test_update_me_password(client, auth_headers):
    resp = client.put(
        "/api/v1/users/me", json={"password": "newpassword123"}, headers=auth_headers
    )
    assert resp.status_code == 200


def test_create_and_list_skills(client, auth_headers):
    create = client.post(
        "/api/v1/users/me/skills",
        json={"name": "Rust", "level": "expert"},
        headers=auth_headers,
    )
    assert create.status_code == 201
    listing = client.get("/api/v1/users/me/skills", headers=auth_headers)
    assert listing.status_code == 200
    assert any(s["name"] == "Rust" for s in listing.json())


def test_remove_skill(client, auth_headers):
    create = client.post(
        "/api/v1/users/me/skills", json={"name": "Go"}, headers=auth_headers
    )
    skill_id = create.json()["id"]
    resp = client.delete(f"/api/v1/users/me/skills/{skill_id}", headers=auth_headers)
    assert resp.status_code == 204


def test_remove_skill_404(client, auth_headers):
    resp = client.delete("/api/v1/users/me/skills/99999", headers=auth_headers)
    assert resp.status_code == 404
