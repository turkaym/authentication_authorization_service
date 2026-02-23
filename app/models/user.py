from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), index=True, unique=True, nullable=False)
    username = Column(String(50), index=True, unique=True, nullable=True)

    password_hash = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    failed_attempts = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)
    lock_until = Column(DateTime(timezone=True), nullable=True)

    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  
        onupdate=func.now())

    role = relationship("Role", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    email_verification_tokens = relationship("EmailVerificationToken", back_populates="user")