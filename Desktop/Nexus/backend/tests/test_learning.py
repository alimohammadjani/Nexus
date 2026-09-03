"""Unit & integration tests for the learning (roadmaps / courses) feature."""

from sqlalchemy import select

from app.crud import learning as crud
from app.models.learning import CourseEnrollment, LessonProgress
from app.models.user import User
from app.schemas.learning import (
    CourseCreate,
    LessonCreate,
    RoadmapCreate,
    RoadmapStageCreate,
)


# ---------------------------------------------------------------------------
# API-level (integration) tests
# ---------------------------------------------------------------------------


def test_list_roadmaps_is_public(client):
    resp = client.get("/api/v1/roadmaps")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_roadmap_404(client):
    resp = client.get("/api/v1/roadmaps/999")
    assert resp.status_code == 404


def test_list_courses_is_public(client):
    resp = client.get("/api/v1/learning/courses")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_course_404(client):
    resp = client.get("/api/v1/learning/courses/999")
    assert resp.status_code == 404


def test_course_category_and_free_filters(client, admin_headers):
    for category, free in [("frontend", True), ("backend", False)]:
        payload = {
            "title": f"Course {category}",
            "description": "desc",
            "category": category,
            "is_free": free,
        }
        assert client.post("/api/v1/learning/courses", json=payload, headers=admin_headers).status_code == 201

    frontend = client.get("/api/v1/learning/courses?category=frontend").json()
    assert all(c["category"] == "frontend" for c in frontend)

    free = client.get("/api/v1/learning/courses?free_only=true").json()
    assert all(c["is_free"] is True for c in free)


def test_create_roadmap_requires_admin(client, auth_headers):
    payload = {
        "title": "RM",
        "description": "d",
        "category": "frontend",
        "color": "#8b5cf6",
        "stages": [{"order": 1, "title": "S1"}],
    }
    resp = client.post("/api/v1/learning/roadmaps", json=payload, headers=auth_headers)
    assert resp.status_code == 403


def test_admin_creates_roadmap_with_stages(client, admin_headers):
    payload = {
        "title": "Frontend Roadmap",
        "subtitle": "sub",
        "description": "desc",
        "category": "frontend",
        "color": "#06b6d4",
        "stages": [
            {
                "order": 1,
                "title": "HTML",
                "description": "d",
                "content": "real training content",
                "resources": "MDN — https://developer.mozilla.org",
                "project": "build a page",
                "checkpoint": "valid HTML",
            },
            {"order": 2, "title": "CSS", "description": "d", "content": "more content"},
        ],
    }
    resp = client.post("/api/v1/learning/roadmaps", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["category"] == "frontend"
    assert len(body["stages"]) == 2
    # the real training content is persisted on each stage
    assert body["stages"][0]["content"] == "real training content"
    assert body["stages"][0]["resources"].startswith("MDN")


def test_create_course_requires_admin(client, auth_headers):
    payload = {"title": "C", "description": "d", "category": "frontend"}
    resp = client.post("/api/v1/learning/courses", json=payload, headers=auth_headers)
    assert resp.status_code == 403


def test_admin_creates_course_with_lessons(client, admin_headers):
    payload = {
        "title": "React Course",
        "description": "desc",
        "category": "frontend",
        "is_free": True,
        "lessons": [
            {"order": 1, "title": "Intro", "content": "lesson content", "duration_minutes": 20},
            {"order": 2, "title": "State", "content": "more", "duration_minutes": 30},
        ],
    }
    resp = client.post("/api/v1/learning/courses", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert len(body["lessons"]) == 2
    assert body["lessons"][0]["content"] == "lesson content"


def test_enroll_is_idempotent(client, admin_headers, auth_headers):
    course = client.post(
        "/api/v1/learning/courses",
        json={"title": "C", "description": "d", "category": "frontend", "lessons": [{"order": 1, "title": "L1"}]},
        headers=admin_headers,
    ).json()
    course_id = course["id"]

    r1 = client.post(f"/api/v1/learning/courses/{course_id}/enroll", headers=auth_headers)
    assert r1.status_code in (200, 201)
    r2 = client.post(f"/api/v1/learning/courses/{course_id}/enroll", headers=auth_headers)
    assert r2.status_code in (200, 201)
    assert r1.json()["id"] == r2.json()["id"]


def test_complete_lesson_updates_progress(client, admin_headers, auth_headers, db_session):
    course = client.post(
        "/api/v1/learning/courses",
        json={
            "title": "Progress Course",
            "description": "d",
            "category": "frontend",
            "lessons": [{"order": i, "title": f"L{i}"} for i in range(1, 5)],
        },
        headers=admin_headers,
    ).json()
    course_id = course["id"]
    lesson_ids = [l["id"] for l in course["lessons"]]

    client.post(f"/api/v1/learning/courses/{course_id}/enroll", headers=auth_headers)
    c1 = client.post(
        f"/api/v1/learning/courses/{course_id}/lessons/{lesson_ids[0]}/complete",
        headers=auth_headers,
    )
    c2 = client.post(
        f"/api/v1/learning/courses/{course_id}/lessons/{lesson_ids[1]}/complete",
        headers=auth_headers,
    )
    assert c1.status_code == 200 and c2.status_code == 200
    # completing the same lesson twice should stay completed, not double count
    c1_again = client.post(
        f"/api/v1/learning/courses/{course_id}/lessons/{lesson_ids[0]}/complete",
        headers=auth_headers,
    )
    assert c1_again.status_code == 200

    enrollment = db_session.execute(
        select(CourseEnrollment).where(CourseEnrollment.course_id == course_id)
    ).scalar_one()
    # 2 of 4 lessons completed -> 0.5 progress
    assert abs(enrollment.progress - 0.5) < 1e-6
    assert enrollment.completed is False


def test_complete_lesson_missing_course(client, auth_headers):
    resp = client.post("/api/v1/learning/courses/999/lessons/1/complete", headers=auth_headers)
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Direct unit tests on the CRUD layer (no HTTP)
# ---------------------------------------------------------------------------


def test_crud_create_roadmap_persists_stages(db_session):
    payload = RoadmapCreate(
        title="Unit RM",
        subtitle="s",
        description="d",
        category="devops",
        color="#10b981",
        stages=[
            RoadmapStageCreate(
                order=1,
                title="Linux",
                description="d",
                content="shell basics",
                resources="linuxjourney",
                project="script",
                checkpoint="runs",
            )
        ],
    )
    roadmap = crud.create_roadmap(db_session, payload)
    db_session.commit()
    db_session.refresh(roadmap)

    assert roadmap.id
    assert len(roadmap.stages) == 1
    assert roadmap.stages[0].content == "shell basics"
    assert roadmap.stages[0].checkpoint == "runs"


def test_crud_lesson_progress_math(db_session):
    user = User(email="learner@example.com", full_name="L", password_hash="x", role="developer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    course = crud.create_course(
        db_session,
        CourseCreate(
            title="C",
            description="d",
            category="mobile",
            lessons=[LessonCreate(order=i, title=f"L{i}") for i in range(1, 5)],
        ),
    )
    db_session.commit()
    db_session.refresh(course)

    enrollment = crud.enroll_user(db_session, course.id, user.id)
    # complete 3 of 4 lessons
    for lesson in course.lessons[:3]:
        crud.mark_lesson_complete(db_session, lesson, user.id)
    crud.update_enrollment_progress(db_session, enrollment, course, user.id)
    db_session.refresh(enrollment)

    assert abs(enrollment.progress - 0.75) < 1e-6
    assert enrollment.completed is False

    # completing the last lesson should mark the course completed
    crud.mark_lesson_complete(db_session, course.lessons[3], user.id)
    crud.update_enrollment_progress(db_session, enrollment, course, user.id)
    db_session.refresh(enrollment)
    assert enrollment.progress == 1.0
    assert enrollment.completed is True


def test_crud_mark_lesson_complete_idempotent(db_session):
    user = User(email="u2@example.com", full_name="U2", password_hash="x", role="developer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    course = crud.create_course(
        db_session,
        CourseCreate(title="C", description="d", category="frontend", lessons=[LessonCreate(order=1, title="L1")]),
    )
    db_session.commit()
    db_session.refresh(course)
    lesson = course.lessons[0]

    p1 = crud.mark_lesson_complete(db_session, lesson, user.id)
    p2 = crud.mark_lesson_complete(db_session, lesson, user.id)
    assert p1.id == p2.id
    # completing twice must not create duplicate progress rows
    total = db_session.execute(
        select(LessonProgress).where(LessonProgress.lesson_id == lesson.id)
    ).scalars().all()
    assert len(total) == 1
    assert total[0].completed is True
