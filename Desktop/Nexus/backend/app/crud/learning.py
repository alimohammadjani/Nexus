"""Learning CRUD helpers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.learning import (
    Course,
    CourseEnrollment,
    Lesson,
    LessonProgress,
    Roadmap,
    RoadmapStage,
)
from app.schemas.learning import (
    CourseCreate,
    CourseUpdate,
    RoadmapCreate,
    RoadmapUpdate,
)


def list_roadmaps(db: Session, category: str | None = None) -> list[Roadmap]:
    stmt = select(Roadmap).where(Roadmap.is_published.is_(True))
    if category:
        stmt = stmt.where(Roadmap.category == category)
    stmt = stmt.order_by(Roadmap.created_at.desc())
    return list(db.scalars(stmt))


def get_roadmap(db: Session, roadmap_id: int) -> Roadmap | None:
    return db.get(Roadmap, roadmap_id)


def create_roadmap(db: Session, data: RoadmapCreate) -> Roadmap:
    roadmap = Roadmap(**data.model_dump(exclude={"stages"}))
    db.add(roadmap)
    db.flush()
    for stage in data.stages:
        db.add(RoadmapStage(roadmap_id=roadmap.id, **stage.model_dump()))
    db.commit()
    db.refresh(roadmap)
    return roadmap


def update_roadmap(db: Session, roadmap: Roadmap, data: RoadmapUpdate) -> Roadmap:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(roadmap, key, value)
    db.commit()
    db.refresh(roadmap)
    return roadmap


def list_courses(db: Session, category: str | None = None, free_only: bool = False) -> list[Course]:
    stmt = select(Course)
    if category:
        stmt = stmt.where(Course.category == category)
    if free_only:
        stmt = stmt.where(Course.is_free.is_(True))
    stmt = stmt.order_by(Course.created_at.desc())
    return list(db.scalars(stmt))


def get_course(db: Session, course_id: int) -> Course | None:
    return db.get(Course, course_id)


def create_course(db: Session, data: CourseCreate) -> Course:
    course = Course(**data.model_dump(exclude={"lessons"}))
    db.add(course)
    db.flush()
    for lesson in data.lessons:
        db.add(Lesson(course_id=course.id, **lesson.model_dump()))
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course: Course, data: CourseUpdate) -> Course:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


def enroll_user(db: Session, course_id: int, user_id: int) -> CourseEnrollment:
    enrollment = db.scalar(
        select(CourseEnrollment).where(
            CourseEnrollment.course_id == course_id, CourseEnrollment.user_id == user_id
        )
    )
    if enrollment:
        return enrollment
    enrollment = CourseEnrollment(course_id=course_id, user_id=user_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def mark_lesson_complete(db: Session, lesson: Lesson, user_id: int, completed: bool = True) -> LessonProgress:
    progress = db.scalar(
        select(LessonProgress).where(LessonProgress.lesson_id == lesson.id, LessonProgress.user_id == user_id)
    )
    if not progress:
        progress = LessonProgress(lesson_id=lesson.id, user_id=user_id)
        db.add(progress)
    progress.completed = completed
    if completed:
        from datetime import datetime

        progress.completed_at = datetime.utcnow()
    else:
        progress.completed_at = None
    db.commit()
    db.refresh(progress)
    return progress


def update_enrollment_progress(db: Session, enrollment: CourseEnrollment, course: Course, user_id: int) -> None:
    from sqlalchemy import func

    lesson_count = len(course.lessons)
    if lesson_count == 0:
        enrollment.progress = 0
    else:
        lesson_ids = [lesson.id for lesson in course.lessons]
        completed_count = db.scalar(
            select(func.count(LessonProgress.id)).where(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id.in_(lesson_ids),
                LessonProgress.completed.is_(True),
            )
        ) or 0
        enrollment.progress = round(completed_count / lesson_count, 3)
    enrollment.completed = enrollment.progress >= 1
    db.commit()
