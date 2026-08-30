"""User CRUD helpers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import Skill, User
from app.schemas.user import SkillCreate, UserRegister, UserUpdate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, data: UserRegister) -> User:
    user = User(
        email=data.email.lower(),
        full_name=data.full_name,
        password_hash=hash_password(data.password),
        role=data.role or "developer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    fields = data.model_dump(exclude_unset=True)
    if "password" in fields and fields["password"]:
        user.password_hash = hash_password(fields.pop("password"))
    for key, value in fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def add_skill(db: Session, user: User, data: SkillCreate) -> Skill:
    skill = Skill(user_id=user.id, name=data.name, level=data.level)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def list_skills(db: Session, user_id: int) -> list[Skill]:
    return list(db.scalars(select(Skill).where(Skill.user_id == user_id).order_by(Skill.name)))


def get_skill(db: Session, skill_id: int) -> Skill | None:
    return db.get(Skill, skill_id)


def delete_skill(db: Session, skill: Skill) -> None:
    db.delete(skill)
    db.commit()
