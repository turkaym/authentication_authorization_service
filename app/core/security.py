import secrets
import hmac
import hashlib
from passlib.context import CryptContext


# ==============================
# Password Hashing (bcrypt)
# ==============================

def get_password_context(rounds: int) -> CryptContext:
    """
    Create a bcrypt password context with configurable rounds.
    """
    return CryptContext(
        schemes=["bcrypt"],
        bcrypt__rounds=rounds,
        deprecated="auto",
    )


def hash_password(password: str, pwd_context: CryptContext) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str, pwd_context: CryptContext) -> bool:
    """
    Verify a plaintext password against a stored bcrypt hash.
    """
    return pwd_context.verify(password, hashed_password)


# ==============================
# Refresh Token Generation
# ==============================

def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure random refresh token.
    64 bytes provides high entropy and strong protection.
    """
    return secrets.token_urlsafe(64)


# ==============================
# HMAC Token Hashing (SHA256)
# ==============================

def hash_token(token: str, secret: str) -> str:
    """
    Hash a token using HMAC-SHA256 with a dedicated secret key.
    This protects against database leaks and precomputation attacks.
    """
    return hmac.new(
        key=secret.encode(),
        msg=token.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

