"""Job endpoint tests."""


def test_create_and_list_jobs(client, auth_headers):
    payload = {
        "title": "Backend Engineer",
        "company": "Acme",
        "description": "Build APIs",
        "skills": "FastAPI,PostgreSQL",
    }
    resp = client.post("/api/v1/jobs", json=payload, headers=auth_headers)
    assert resp.status_code == 201, resp.text

    listing = client.get("/api/v1/jobs")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_get_job_increments_views(client, auth_headers):
    payload = {
        "title": "Frontend Engineer",
        "company": "Acme",
        "description": "Build UIs",
    }
    job_id = client.post("/api/v1/jobs", json=payload, headers=auth_headers).json()["id"]
    first = client.get(f"/api/v1/jobs/{job_id}").json()
    second = client.get(f"/api/v1/jobs/{job_id}").json()
    assert second["views"] == first["views"] + 1


def test_apply_to_job(client, auth_headers):
    payload = {
        "title": "Data Engineer",
        "company": "Acme",
        "description": "Build pipelines",
    }
    job_id = client.post("/api/v1/jobs", json=payload, headers=auth_headers).json()["id"]
    resp = client.post(
        f"/api/v1/jobs/{job_id}/apply",
        json={"cover_letter": "Hello, I'm interested."},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "applied"


def test_unauthenticated_job_create(client):
    resp = client.post(
        "/api/v1/jobs", json={"title": "x", "company": "y", "description": "z"}
    )
    assert resp.status_code == 401
