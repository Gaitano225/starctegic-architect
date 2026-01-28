from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.subscription import Subscription as SubscriptionModel, PlanType
from app.schemas.subscription import Subscription, SubscriptionUpdate

router = APIRouter()

@router.get("/me", response_model=Subscription)
def read_my_subscription(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's subscription status.
    """
    subscription = db.query(SubscriptionModel).filter(SubscriptionModel.user_id == current_user.id).first()
    if not subscription:
        # Create a default founder subscription if none exists
        subscription = SubscriptionModel(
            user_id=current_user.id,
            plan=PlanType.FOUNDER,
            reports_limit=3
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    return subscription

@router.post("/upgrade")
def upgrade_plan(
    plan: PlanType,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mock upgrade plan endpoint. Actual upgrade would happen after payment.
    """
    subscription = db.query(SubscriptionModel).filter(SubscriptionModel.user_id == current_user.id).first()
    if not subscription:
        subscription = SubscriptionModel(user_id=current_user.id)
        db.add(subscription)
    
    subscription.plan = plan
    if plan == PlanType.STRATEGIST:
        subscription.reports_limit = 10
    elif plan == PlanType.VISIONARY:
        subscription.reports_limit = 9999 # Unlimited
    
    db.add(subscription)
    db.commit()
    return {"message": f"Successfully upgraded to {plan}"}
