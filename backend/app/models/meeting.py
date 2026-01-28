from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Expert Consultation (30 min)")
    description = Column(Text, nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="pending") # pending, confirmed, cancelled, completed
    
    user = relationship("User", backref="meetings")
