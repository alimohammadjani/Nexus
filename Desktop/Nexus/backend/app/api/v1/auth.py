"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.crud.user import create_user, get_user_by_email, get_user_by_id
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import LoginResponse, UserLogin, UserOut, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> User:
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return create_user(db, payload)


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
