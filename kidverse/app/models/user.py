from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

AGE_GROUPS = ("toddler", "explorer", "creator")


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(100), nullable=False)
    avatar        = Column(String(50),  default="star")
    age_group     = Column(String(20),  default="creator", server_default="creator")
    points        = Column(Integer,     default=0)
    level         = Column(Integer,     default=1)
    created_at    = Column(DateTime,    default=datetime.utcnow)

    # ── Auth fields ───────────────────────────────────────────────────────────
    email         = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)
    phone         = Column(String(20),  nullable=True)
    is_verified   = Column(Boolean,     default=False, server_default="0")
    otp_code      = Column(String(6),   nullable=True)
    otp_expires_at = Column(DateTime,   nullable=True)

    activities = relationship("Activity", back_populates="user")