from typing import Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.api import deps
# from app.models.user import User  # Supprimé pour éviter import circulaire
from app.models.meeting import Meeting
from app.services.notification_service import NotificationService

router = APIRouter()

class MeetingCreate(BaseModel):
    scheduled_at: datetime
    notes: Optional[str] = None

class FeedbackCreate(BaseModel):
    rating: int
    comment: str
    email: Optional[EmailStr] = None

@router.post("/book-session")
def book_session(
    *,
    db: Session = Depends(deps.get_db),
    meeting_in: MeetingCreate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    from app.models.user import User  # Import local pour éviter NameError circulaire
    """
    Book a 30-min expert consultation.
    """
    # Check if slot is in the future
    if meeting_in.scheduled_at < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book in the past")

    meeting = Meeting(
        user_id=current_user.id,
        scheduled_at=meeting_in.scheduled_at,
        description=meeting_in.notes
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    # Notify Admin
    NotificationService.notify_admin(
        db, 
        "Nouveau RDV Expert", 
        f"L'utilisateur {current_user.email} a réservé une session pour le {meeting.scheduled_at}."
    )
    
    # Notify User
    NotificationService.create_notification(
        db, 
        current_user.id, 
        "RDV Confirmé", 
        f"Votre session expert de 30 min est réservée pour le {meeting.scheduled_at}. Un lien vous sera envoyé."
    )
    
    return meeting

@router.post("/feedback")
def send_feedback(
    *,
    db: Session = Depends(deps.get_db),
    feedback: FeedbackCreate,
    current_user: Any = Depends(deps.get_current_user_optional)
) -> Any:
    from app.models.user import User  # Import local pour éviter NameError circulaire
    """
    Send feedback via a form.
    """
    user_email = current_user.email if current_user else feedback.email or "Anonyme"
    
    # Trigger notification for Admin
    NotificationService.notify_admin(
        db, 
        "Nouveau Feedback Client", 
        f"De: {user_email}\nNote: {feedback.rating}/5\nCommentaire: {feedback.comment}"
    )
    
    # In a real app, send mail directly to the master email
    print(f"FEEDBACK RECEIVED from {user_email}: {feedback.comment}")
    
    return {"message": "Merci pour votre retour !"}
