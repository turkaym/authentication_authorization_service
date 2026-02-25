from typing import Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.jwt import decode_access_token
from app.core.config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token_payload(
        token: str = Depends(oauth2_schema)
) -> Dict[str, Any]:
    """
    Decode and validate JWT access token.
    """

    try:
        payload = decode_access_token(
            token=token,
            secret=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
        payload: Dict[str, Any] = Depends(get_token_payload)
) -> Dict[str, Any]:
    """
    Extract user information from token payload.
    """

    user_id = payload.get("sub")
    role = payload.get("role")

    if user_id is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token payload",
        )

    return {
        "user_id": int(user_id),
        "role": role,
        "jti": payload.get("jti"),
    }


def required_role(required_role: str):
    """
    Role-based access dependency factory.
    """

    def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_user),
    ):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
