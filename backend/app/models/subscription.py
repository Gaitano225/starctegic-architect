from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class PlanType(str, enum.Enum):
    FOUNDER = "fondateur"
    STRATEGIST = "stratege"
    VISIONARY = "visionnaire"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(String, default=PlanType.FOUNDER)
    
    # Limits
    reports_limit = Column(Integer, default=3)
    reports_generated = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="subscription")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
