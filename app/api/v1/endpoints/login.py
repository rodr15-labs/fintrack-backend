from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.errors import ErrorCode
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail=ErrorCode.INVALID_CREDENTIALS)

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=UserResponse)
def create_user(*, db: Session = Depends(deps.get_db), user_in: UserCreate):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail=ErrorCode.EMAIL_ALREADY_EXISTS)

    db_obj = User(
        email=user_in.email,
        username=user_in.username,
        password=get_password_hash(user_in.password),
        is_active=True,
    )
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=ErrorCode.USER_CREATION_FAILED)
