"""Learning models: roadmaps, courses, lessons and progress."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    subtitle: Mapped[str | None] = Column(String(512), nullable=True)
    description: Mapped[str | None] = Column(Text, nullable=True)
    category: Mapped[str] = Column(String(64), default="backend", index=True)
    color: Mapped[str | None] = Column(String(16), nullable=True)
    is_published: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    stages = relationship("RoadmapStage", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapStage(Base):
    __tablename__ = "roadmap_stages"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    roadmap_id: Mapped[int] = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True)
    order: Mapped[int] = Column(Integer, default=0, nullable=False)
    title: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str | None] = Column(Text, nullable=True)
    resources: Mapped[str | None] = Column(Text, nullable=True)
    project: Mapped[str | None] = Column(Text, nullable=True)
    checkpoint: Mapped[str | None] = Column(Text, nullable=True)

    roadmap = relationship("Roadmap", back_populates="stages")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    category: Mapped[str] = Column(String(64), index=True)
    level: Mapped[str] = Column(String(64), default="beginner")
    instructor_name: Mapped[str | None] = Column(String(255), nullable=True)
    cover_url: Mapped[str | None] = Column(String(512), nullable=True)
    duration_hours: Mapped[float] = Column(Float, default=0, nullable=False)
    is_free: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    price: Mapped[float] = Column(Float, default=0, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    order: Mapped[int] = Column(Integer, default=0, nullable=False)
    title: Mapped[str] = Column(String(255), nullable=False)
    content: Mapped[str | None] = Column(Text, nullable=True)
    video_url: Mapped[str | None] = Column(String(512), nullable=True)
    duration_minutes: Mapped[int] = Column(Integer, default=0, nullable=False)

    course = relationship("Course", back_populates="lessons")


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    __table_args__ = (UniqueConstraint("course_id", "user_id", name="uq_enrollment_course_user"),)

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    progress: Mapped[float] = Column(Float, default=0, nullable=False)
    completed: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    enrolled_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    course = relationship("Course")
    user = relationship("User")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("lesson_id", "user_id", name="uq_lesson_progress_user"),)

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    completed: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = Column(DateTime, nullable=True)

    lesson = relationship("Lesson")
