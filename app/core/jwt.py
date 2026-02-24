from datetime import datetime, timedelta, timezone  
from uuid import uuid4  
from typing import Any, Dict  
  
from jose import JWTError, jwt

# ==============================
# JTI Generator
# ==============================

def generate_jti() -> str:
    """
    Generate a unique token identifier.
    Used for blacklisting and auditing.
    """
    return str(uuid4())


# ==============================
# Access Token Creation
# ==============================

def create_access_token(
    user_id: int,
    role: str,
    secret: str,
    algorithm: str,
    expire_minutes: int,
) -> str:
    """
    Create a signed JWT access token.
    """

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "jti": generate_jti(),
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, secret, algorithm=algorithm)


# ==============================
# Token Decoding
# ==============================

def decode_access_token(
    token: str,
    secret: str,
    algorithm: str,
) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    Raises JWTError if invalid.
    """

    return jwt.decode(token, secret, algorithms=[algorithm])