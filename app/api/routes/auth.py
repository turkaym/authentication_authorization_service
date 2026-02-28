from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import authenticate_user, refresh_access_token
from app.schemas.auth import TokenResponse, RefreshRequest


router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return authenticate_user(
        db=db,
        identifier=form_data.username,
        password=form_data.password,
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        db=db,
        refresh_token=request.refresh_token,
    )
