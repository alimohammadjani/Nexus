"""Extra job endpoint tests (auth, filters, applications)."""


def test_get_job_404(client):
    resp = client.get("/api/v1/jobs/99999")
    assert resp.status_code == 404


def test_update_job_404(client, auth_headers):
    resp = client.put("/api/v1/jobs/99999", json={"title": "x"}, headers=auth_headers)
    assert resp.status_code == 404


def test_apply_job_404(client, auth_headers):
    resp = client.post(
        "/api/v1/jobs/99999/apply", json={"cover_letter": "x"}, headers=auth_headers
    )
    assert resp.status_code == 404


def test_update_job_owner(client, auth_headers):
    job_id = client.post(
        "/api/v1/jobs",
        json={"title": "J", "company": "C", "description": "d"},
        headers=auth_headers,
    ).json()["id"]
    resp = client.put(f"/api/v1/jobs/{job_id}", json={"title": "Updated"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"


def test_update_job_other_forbidden(client, auth_headers, register_user):
    job_id = client.post(
        "/api/v1/jobs",
        json={"title": "J", "company": "C", "description": "d"},
        headers=auth_headers,
    ).json()["id"]
    other = register_user("recruiter2@example.com")
    resp = client.put(f"/api/v1/jobs/{job_id}", json={"title": "X"}, headers=other)
    assert resp.status_code == 403


def test_delete_job_owner(client, auth_headers):
    job_id = client.post(
        "/api/v1/jobs",
        json={"title": "J", "company": "C", "description": "d"},
        headers=auth_headers,
    ).json()["id"]
    resp = client.delete(f"/api/v1/jobs/{job_id}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_job_404(client, auth_headers):
    resp = client.delete("/api/v1/jobs/99999", headers=auth_headers)
    assert resp.status_code == 404


def test_job_applications_owner(client, auth_headers):
    job_id = client.post(
        "/api/v1/jobs",
        json={"title": "J", "company": "C", "description": "d"},
        headers=auth_headers,
    ).json()["id"]
    client.post(
        f"/api/v1/jobs/{job_id}/apply",
        json={"cover_letter": "hi"},
        headers=auth_headers,
    )
    resp = client.get(f"/api/v1/jobs/{job_id}/applications", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_job_applications_other_forbidden(client, auth_headers, register_user):
    job_id = client.post(
        "/api/v1/jobs",
        json={"title": "J", "company": "C", "description": "d"},
        headers=auth_headers,
    ).json()["id"]
    other = register_user("recruiter3@example.com")
    resp = client.get(f"/api/v1/jobs/{job_id}/applications", headers=other)
    assert resp.status_code == 403


def test_job_applications_404(client, auth_headers):
    resp = client.get("/api/v1/jobs/99999/applications", headers=auth_headers)
    assert resp.status_code == 404


def test_list_jobs_filters(client, auth_headers):
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Dev",
            "company": "Acme",
            "description": "d",
            "skills": "Python,Django",
            "type": "full_time",
            "mode": "remote",
            "level": "senior",
        },
        headers=auth_headers,
    )
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Go Dev",
            "company": "Beta",
            "description": "d",
            "skills": "Go",
            "type": "contract",
            "mode": "hybrid",
            "level": "junior",
        },
        headers=auth_headers,
    )
    by_search = client.get("/api/v1/jobs?search=Python").json()
    assert len(by_search) == 1 and by_search[0]["title"] == "Python Dev"
    by_skill = client.get("/api/v1/jobs?skill=Django").json()
    assert len(by_skill) == 1
    by_type = client.get("/api/v1/jobs?type=contract").json()
    assert len(by_type) == 1 and by_type[0]["type"] == "contract"
    by_mode = client.get("/api/v1/jobs?mode=hybrid").json()
    assert len(by_mode) == 1
    by_level = client.get("/api/v1/jobs?level=junior").json()
    assert len(by_level) == 1
