from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from app.schemas.user import UserLogin
from app.schemas.token import RefreshRequest

from app.services.user_service import authenticate_user
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.services.user_service import (
    get_user_by_email,
    create_user,
)

router = APIRouter()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    existing = get_user_by_email(db, user.email)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    new_user = create_user(
        db,
        email=user.email,
        username=user.username,
        password=user.password,
    )

    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        form_data.username,   # username field will contain the email
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


    access_token = create_access_token(
    {"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    payload = verify_refresh_token(
        data.refresh_token
    )

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(
        {
            "sub": payload["sub"],
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
