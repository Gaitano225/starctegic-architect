from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
# from app.models.user import User  # Supprimé pour éviter l'import circulaire
from app.models.project import Project
from app.schemas.user import User as UserSchema

from app.models.subscription import Subscription as SubscriptionModel
from app.services.notification_service import NotificationService

router = APIRouter()

@router.get("/subscriptions")
def read_all_subscriptions(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return db.query(SubscriptionModel).all()

@router.post("/subscriptions/{subscription_id}/toggle")
def toggle_subscription(
    subscription_id: int,
    is_active: bool,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    subscription = db.query(SubscriptionModel).filter(SubscriptionModel.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.is_active = is_active
    db.commit()
    
    status_msg = "activé" if is_active else "désactivé"
    # Notify user
    NotificationService.create_notification(
        db, 
        subscription.user_id, 
        "Statut de votre abonnement", 
        f"Votre abonnement a été {status_msg} par l'administrateur."
    )
    
    return {"message": f"Subscription {status_msg}"}

@router.get("/notifications")
def read_admin_notifications(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return NotificationService.get_admin_notifications(db)
