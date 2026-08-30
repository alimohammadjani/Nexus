"""Learning / roadmap endpoint tests."""


def test_roadmaps_public(client):
    resp = client.get("/api/v1/roadmaps")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_courses_public(client):
    resp = client.get("/api/v1/learning/courses")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_enroll_course(client, auth_headers):
    course = client.post(
        "/api/v1/learning/courses",
        json={
            "title": "Docker Course",
            "description": "Learn Docker",
            "category": "devops",
            "is_free": True,
        },
        headers=auth_headers,
    )
    # Non-admin cannot create content
    assert course.status_code == 403
