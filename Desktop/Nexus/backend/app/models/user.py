"""User and skill models."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = Column(String(255), nullable=False)
    password_hash: Mapped[str] = Column(String(512), nullable=False)
    role: Mapped[str] = Column(String(32), default="developer", nullable=False)
    bio: Mapped[str | None] = Column(Text, nullable=True)
    avatar_url: Mapped[str | None] = Column(String(512), nullable=True)
    location: Mapped[str | None] = Column(String(255), nullable=True)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_employer: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    company: Mapped[str | None] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="owner", foreign_keys="Job.owner_id")
    applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=False)
    level: Mapped[str] = Column(String(32), default="beginner", nullable=False)

    user = relationship("User", back_populates="skills")
