"""Learning endpoints: roadmaps and courses."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import learning as crud
from app.database import get_db
from app.dependencies import get_current_user
from app.models.learning import Course, CourseEnrollment, Lesson, Roadmap
from app.models.user import User
from app.schemas.learning import (
    CourseCreate,
    CourseUpdate,
    CourseOut,
    EnrollmentOut,
    LessonProgressOut,
    RoadmapCreate,
    RoadmapOut,
    RoadmapUpdate,
)

router = APIRouter(prefix="/learning", tags=["learning"])


# --- Roadmaps ---


@router.get("/roadmaps", response_model=list[RoadmapOut])
def list_roadmaps(
    category: str | None = Query(default=None), db: Session = Depends(get_db)
):
    return crud.list_roadmaps(db, category=category)


@router.post("/roadmaps", response_model=RoadmapOut, status_code=status.HTTP_201_CREATED)
def create_roadmap(
    payload: RoadmapCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Roadmap:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return crud.create_roadmap(db, payload)


@router.get("/roadmaps/{roadmap_id}", response_model=RoadmapOut)
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)) -> Roadmap:
    roadmap = crud.get_roadmap(db, roadmap_id)
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    return roadmap


@router.put("/roadmaps/{roadmap_id}", response_model=RoadmapOut)
def update_roadmap(
    roadmap_id: int,
    payload: RoadmapUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Roadmap:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    roadmap = crud.get_roadmap(db, roadmap_id)
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    return crud.update_roadmap(db, roadmap, payload)


# --- Courses ---


@router.get("/courses", response_model=list[CourseOut])
def list_courses(
    category: str | None = Query(default=None),
    free_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    return crud.list_courses(db, category=category, free_only=free_only)


@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Course:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return crud.create_course(db, payload)


@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)) -> Course:
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.put("/courses/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Course:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return crud.update_course(db, course, payload)


@router.post("/courses/{course_id}/enroll", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def enroll(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CourseEnrollment:
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return crud.enroll_user(db, course_id, current_user.id)


@router.post("/courses/{course_id}/lessons/{lesson_id}/complete", response_model=LessonProgressOut)
def complete_lesson(
    course_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    lesson = next((l for l in course.lessons if l.id == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    enrollment = crud.enroll_user(db, course_id, current_user.id)
    progress = crud.mark_lesson_complete(db, lesson, current_user.id)
    crud.update_enrollment_progress(db, enrollment, course, current_user.id)
    return progress
