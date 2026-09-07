"""Direct unit tests for app.crud.user."""

from app.crud import user as crud
from app.models.user import User
from app.schemas.user import SkillCreate, UserRegister, UserUpdate


def test_create_and_fetch_user(db_session):
    user = crud.create_user(
        db_session, UserRegister(email="crud@example.com", full_name="C", password="password123")
    )
    assert user.id
    # email lookup is normalised to lower-case
    assert crud.get_user_by_email(db_session, "CRUD@EXAMPLE.COM") is not None
    assert crud.get_user_by_id(db_session, user.id).id == user.id


def test_update_user_password_hashed(db_session):
    user = crud.create_user(
        db_session, UserRegister(email="u1@example.com", full_name="U", password="password123")
    )
    crud.update_user(db_session, user, UserUpdate(password="newpassword123"))
    db_session.refresh(user)
    # password must be hashed, never stored in plain text
    assert user.password_hash != "newpassword123"
    assert len(user.password_hash) > 20


def test_update_user_fields(db_session):
    user = crud.create_user(
        db_session, UserRegister(email="u2@example.com", full_name="U", password="password123")
    )
    crud.update_user(db_session, user, UserUpdate(full_name="Updated", bio="hello"))
    db_session.refresh(user)
    assert user.full_name == "Updated"
    assert user.bio == "hello"


def test_skill_crud(db_session):
    user = crud.create_user(
        db_session, UserRegister(email="u3@example.com", full_name="U", password="password123")
    )
    skill = crud.add_skill(db_session, user, SkillCreate(name="TS", level="expert"))
    assert skill.id
    assert skill.name == "TS"
    skills = crud.list_skills(db_session, user.id)
    assert len(skills) == 1
    assert crud.get_skill(db_session, skill.id).id == skill.id
    crud.delete_skill(db_session, skill)
    assert crud.get_skill(db_session, skill.id) is None
