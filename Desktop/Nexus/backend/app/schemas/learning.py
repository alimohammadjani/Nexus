"""Learning related schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# --- Roadmaps ---


class RoadmapStageBase(BaseModel):
    order: int = 0
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    resources: str | None = None
    project: str | None = None
    checkpoint: str | None = None


class RoadmapStageCreate(RoadmapStageBase):
    pass


class RoadmapStageOut(RoadmapStageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    roadmap_id: int


class RoadmapBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    subtitle: str | None = None
    description: str | None = None
    category: str = "backend"
    color: str | None = None


class RoadmapCreate(RoadmapBase):
    stages: list[RoadmapStageCreate] = []


class RoadmapUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None
    category: str | None = None
    color: str | None = None
    is_published: bool | None = None


class RoadmapOut(RoadmapBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_published: bool
    created_at: datetime
    stages: list[RoadmapStageOut] = []


# --- Courses ---


class LessonBase(BaseModel):
    order: int = 0
    title: str = Field(..., min_length=1, max_length=255)
    content: str | None = None
    video_url: str | None = None
    duration_minutes: int = 0


class LessonCreate(LessonBase):
    pass


class LessonOut(LessonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    category: str = "backend"
    level: str = "beginner"
    instructor_name: str | None = None
    cover_url: str | None = None
    duration_hours: float = 0
    is_free: bool = True
    price: float = 0


class CourseCreate(CourseBase):
    lessons: list[LessonCreate] = []


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    level: str | None = None
    instructor_name: str | None = None
    cover_url: str | None = None
    duration_hours: float | None = None
    is_free: bool | None = None
    price: float | None = None


class CourseOut(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    lessons: list[LessonOut] = []


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    user_id: int
    progress: float
    completed: bool
    enrolled_at: datetime


class LessonProgressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    user_id: int
    completed: bool
    completed_at: datetime | None
