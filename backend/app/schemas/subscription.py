from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.subscription import PlanType

class SubscriptionBase(BaseModel):
    plan: PlanType = PlanType.FOUNDER
    reports_limit: int = 3
    is_active: bool = True

class SubscriptionCreate(SubscriptionBase):
    user_id: int

class SubscriptionUpdate(BaseModel):
    plan: Optional[PlanType] = None
    reports_limit: Optional[int] = None
    reports_generated: Optional[int] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class Subscription(SubscriptionBase):
    id: int
    user_id: int
    reports_generated: int
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
