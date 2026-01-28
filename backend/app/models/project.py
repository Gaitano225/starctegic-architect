from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Store answers as a JSON object: {"q1": "BJ", "q2": "ecommerce", ...}
    answers = Column(JSON, default={})
    
    # Store recommendations as a JSON list of rule objects
    recommendations = Column(JSON, default=[])

    # Store IDs of rules that were triggered for audit trail
    applied_rule_ids = Column(JSON, default=[])
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
