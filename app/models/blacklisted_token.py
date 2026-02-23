from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)

    token_hash = Column(String(255), nullable=False, index=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())
