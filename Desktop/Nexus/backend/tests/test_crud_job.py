"""Direct unit tests for app.crud.job."""

from app.crud import job as crud
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate


def _make_owner(db_session):
    owner = User(email="jobowner@example.com", full_name="O", password_hash="x", role="employer")
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner


def test_list_jobs_filters(db_session):
    owner = _make_owner(db_session)
    crud.create_job(
        db_session,
        owner.id,
        JobCreate(
            title="Python Job",
            company="A",
            description="d",
            skills="Python",
            type="full_time",
            mode="remote",
            level="senior",
        ),
    )
    crud.create_job(
        db_session,
        owner.id,
        JobCreate(
            title="Go Job",
            company="B",
            description="d",
            skills="Go",
            type="contract",
            mode="hybrid",
            level="junior",
        ),
    )
    assert len(crud.list_jobs(db_session, search="Python")) == 1
    assert len(crud.list_jobs(db_session, skill="Go")) == 1
    assert len(crud.list_jobs(db_session, job_type="contract")) == 1
    assert len(crud.list_jobs(db_session, mode="hybrid")) == 1
    assert len(crud.list_jobs(db_session, level="junior")) == 1


def test_job_lifecycle(db_session):
    owner = _make_owner(db_session)
    job = crud.create_job(db_session, owner.id, JobCreate(title="J", company="C", description="d"))
    assert job.id
    updated = crud.update_job(db_session, job, JobUpdate(title="J2", is_active=False))
    assert updated.title == "J2"
    assert updated.is_active is False
    application = crud.apply_to_job(db_session, job.id, owner.id, "cover")
    assert application.id and application.status == "applied"
    apps = crud.list_applications(db_session, job_id=job.id)
    assert len(apps) == 1
    crud.delete_job(db_session, job)
    assert crud.get_job(db_session, job.id) is None
