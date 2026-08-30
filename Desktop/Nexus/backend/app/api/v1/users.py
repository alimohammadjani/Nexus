"""User profile endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.user import (
    add_skill,
    delete_skill,
    get_skill,
    get_user_by_id,
    list_skills,
    update_user as update_user_crud,
)
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import Skill, User
from app.schemas.user import SkillCreate, SkillOut, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(User).where(User.is_active.is_(True))
    if search:
        stmt = stmt.where(User.full_name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
    return list(db.scalars(stmt.order_by(User.created_at.desc())))


@router.get("/me", response_model=UserOut)
def my_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    return update_user_crud(db, current_user, payload)


@router.post("/me/skills", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(
    payload: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Skill:
    return add_skill(db, current_user, payload)


@router.get("/me/skills", response_model=list[SkillOut])
def my_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_skills(db, current_user.id)


@router.delete("/me/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skill = get_skill(db, skill_id)
    if not skill or skill.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    delete_skill(db, skill)
