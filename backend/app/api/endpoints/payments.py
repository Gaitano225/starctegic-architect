from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
import json

from app.api import deps
from app.models.subscription import Subscription, PlanType
# from app.models.user import User  # Supprimé pour éviter l'import circulaire

router = APIRouter()

@router.post("/fedapay/webhook")
async def fedapay_webhook(
    request: Request,
    db: Session = Depends(deps.get_db),
    x_fedapay_signature: str = Header(None)
) -> Any:
    """
    Webhook handler for Fedapay payments.
    """
    payload = await request.body()
    # In production, verify signature here
    
    try:
        data = json.loads(payload)
        event = data.get("event")
        
        if event == "transaction.approved":
            # Extract user_id and plan from metadata
            metadata = data.get("transaction", {}).get("metadata", {})
            user_id = metadata.get("user_id")
            plan_name = metadata.get("plan")
            
            if user_id and plan_name:
                subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
                if not subscription:
                    subscription = Subscription(user_id=user_id)
                    db.add(subscription)
                
                subscription.plan = plan_name
                # Update limits based on plan
                if plan_name == PlanType.STRATEGIST:
                    subscription.reports_limit = 10
                elif plan_name == PlanType.VISIONARY:
                    subscription.reports_limit = 9999
                
                db.add(subscription)
                db.commit()
                
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/kkapay/webhook")
async def kkapay_webhook(
    request: Request,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Webhook handler for Kkapay payments.
    """
    payload = await request.json()
    # Logic similar to Fedapay, adapted to Kkapay's payload structure
    return {"status": "success"}
