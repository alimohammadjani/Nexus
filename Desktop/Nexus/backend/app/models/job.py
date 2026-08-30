"""Job postings and applications."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    company: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    location: Mapped[str | None] = Column(String(255), nullable=True)
    type: Mapped[str] = Column(String(64), default="full_time")  # full_time, part_time, freelance, contract
    mode: Mapped[str] = Column(String(64), default="remote")  # remote, hybrid, on_site
    level: Mapped[str] = Column(String(64), default="mid")
    salary_range: Mapped[str | None] = Column(String(128), nullable=True)
    skills: Mapped[str] = Column(Text, default="", nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_featured: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    budget: Mapped[float | None] = Column(Float, nullable=True)
    views: Mapped[int] = Column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    owner = relationship("User", back_populates="jobs", foreign_keys=[owner_id])
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    job_id: Mapped[int] = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = Column(String(64), default="applied")  # applied, reviewed, interview, offer, rejected
    cover_letter: Mapped[str | None] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")
