"""User related schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: str = Field(default="beginner", max_length=32)


class SkillCreate(SkillBase):
    pass


class SkillOut(SkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    bio: str | None = None
    avatar_url: str | None = None
    location: str | None = None


class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="developer", max_length=32)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    bio: str | None = None
    avatar_url: str | None = None
    location: str | None = None
    is_employer: bool | None = None
    company: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
    is_verified: bool
    is_employer: bool
    company: str | None = None
    skills: list[SkillOut] = []
    created_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
