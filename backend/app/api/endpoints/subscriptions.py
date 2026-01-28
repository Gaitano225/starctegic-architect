from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
# from app.models.user import User  # Supprimé pour éviter import circulaire
from app.models.subscription import Subscription as SubscriptionModel, PlanType
from app.schemas.subscription import Subscription, SubscriptionUpdate

router = APIRouter()

@router.get("/me", response_model=Subscription)
def read_my_subscription(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    from app.models.user import User  # Import local pour éviter NameError circulaires
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
    current_user: Any = Depends(deps.get_current_active_user),
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
    
    subscription.is_active = True
    expiry_date = datetime.now() + timedelta(days=30)
    subscription.expires_at = expiry_date

    db.add(subscription)
    db.commit()

    # Trigger Notifications
    from app.services.notification_service import NotificationService
    NotificationService.notify_admin(
        db, 
        "Paiement Reçu / Abonnement", 
        f"L'utilisateur {current_user.email} a activé le pack {plan}."
    )
    NotificationService.create_notification(
        db, 
        current_user.id, 
        "Abonnement Activé", 
        f"Votre pack {plan} est actif jusqu'au {expiry_date.strftime('%d/%m/%Y')}. Merci de votre confiance !"
    )

    return {"message": f"Successfully upgraded to {plan}"}
