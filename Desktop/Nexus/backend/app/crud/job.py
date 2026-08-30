"""Job CRUD helpers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job, JobApplication
from app.schemas.job import JobCreate, JobUpdate


def list_jobs(
    db: Session,
    search: str | None = None,
    skill: str | None = None,
    job_type: str | None = None,
    mode: str | None = None,
    level: str | None = None,
) -> list[Job]:
    stmt = select(Job).where(Job.is_active.is_(True))
    if search:
        stmt = stmt.where(Job.title.ilike(f"%{search}%") | Job.company.ilike(f"%{search}%"))
    if skill:
        stmt = stmt.where(Job.skills.ilike(f"%{skill}%"))
    if job_type:
        stmt = stmt.where(Job.type == job_type)
    if mode:
        stmt = stmt.where(Job.mode == mode)
    if level:
        stmt = stmt.where(Job.level == level)
    stmt = stmt.order_by(Job.is_featured.desc(), Job.created_at.desc())
    return list(db.scalars(stmt))


def get_job(db: Session, job_id: int) -> Job | None:
    return db.get(Job, job_id)


def create_job(db: Session, owner_id: int, data: JobCreate) -> Job:
    job = Job(owner_id=owner_id, **data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job: Job, data: JobUpdate) -> Job:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()


def apply_to_job(db: Session, job_id: int, candidate_id: int, cover_letter: str | None) -> JobApplication:
    app = JobApplication(job_id=job_id, candidate_id=candidate_id, cover_letter=cover_letter)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def list_applications(db: Session, **filters) -> list[JobApplication]:
    stmt = select(JobApplication)
    for key, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(JobApplication, key) == value)
    stmt = stmt.order_by(JobApplication.created_at.desc())
    return list(db.scalars(stmt))
