"""Job schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    location: str | None = None
    type: str = Field(default="full_time", max_length=64)
    mode: str = Field(default="remote", max_length=64)
    level: str = Field(default="mid", max_length=64)
    salary_range: str | None = None
    skills: str = ""
    budget: float | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    description: str | None = None
    location: str | None = None
    type: str | None = None
    mode: str | None = None
    level: str | None = None
    salary_range: str | None = None
    skills: str | None = None
    budget: float | None = None
    is_active: bool | None = None


class JobOut(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    is_active: bool
    is_featured: bool
    views: int
    created_at: datetime
    updated_at: datetime


class ApplicationCreate(BaseModel):
    cover_letter: str | None = None


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    candidate_id: int
    status: str
    cover_letter: str | None = None
    created_at: datetime
    updated_at: datetime
