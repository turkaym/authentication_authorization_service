from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    get_password_context,
    verify_password,
    generate_refresh_token,
    hash_token,
)
from app.core.jwt import create_access_token
from app.core.config import settings


# Dummy hash to prevent timing attacks
DUMMY_HASH = get_password_context(settings.bcrypt_rounds).hash("dummy_password")


def authenticate_user(
    db: Session,
    identifier: str,
    password: str,
):
    pwd_context = get_password_context(settings.bcrypt_rounds)

    user = db.query(User).filter(
        or_(
            User.email == identifier,
            User.username == identifier
        )
    ).first()

    if not user:
        # fake verification to prevent timing attack
        verify_password(password, DUMMY_HASH, pwd_context)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Check account lock
    now = datetime.utcnow()

    if user.is_locked and user.lock_until and now < user.lock_until:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is temporarily locked",
        )

    if not verify_password(password, user.password_hash, pwd_context):
        user.failed_attempts += 1

        if user.failed_attempts >= settings.account_login_attempts:
            user.is_locked = True
            user.lock_until = now + timedelta(minutes=settings.account_lock_minutes)

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Successful login
    user.failed_attempts = 0
    user.is_locked = False
    user.lock_until = None
    user.last_login_at = now

    db.commit()

    # Generate tokens
    access_token = create_access_token(
        user_id=user.id,
        role=user.role.name,
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.access_token_expire_minutes,
    )

    refresh_token = generate_refresh_token()

    refresh_token_hash = hash_token(
        refresh_token,
        settings.token_hash_secret,
    )

    refresh_expires = now + timedelta(days=settings.refresh_token_expire_days)

    db_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=refresh_token_hash,
        expires_at=refresh_expires,
        revoked=False,
    )

    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(
    db: Session,
    refresh_token: str,
):
    now = datetime.utcnow()

    token_hash = hash_token(
        refresh_token,
        settings.token_hash_secret,
    )

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if db_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked",
        )

    if now > db_token.expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    user = db_token.user

    # ROTATE (critical)
    db_token.revoked = True
    db.commit()

    new_access_token = create_access_token(
        user_id=user.id,
        role=user.role.name,
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.access_token_expire_minutes,
    )

    new_refresh_token = generate_refresh_token()
    new_refresh_hash = hash_token(
        new_refresh_token,
        settings.token_hash_secret,
    )

    new_expires = now + timedelta(days=settings.refresh_token_expire_days)

    db_new_refresh = RefreshToken(
        user_id=user.id,
        token_hash=new_refresh_hash,
        expires_at=new_expires,
        revoked=False,
    )

    db.add(db_new_refresh)
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }