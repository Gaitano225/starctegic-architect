from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session, 
        user_id: Optional[int], 
        title: str, 
        message: str
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        # In a real app, this is where you'd send an email via SMTP/SendGrid
        print(f"NOTIFICATION [{title}] for User {user_id}: {message}")
        return notification

    @staticmethod
    def notify_admin(db: Session, title: str, message: str):
        """
        Envoie une notification admin ET un email à tomgaitano78@mail.com
        """
        notification = NotificationService.create_notification(db, None, title, message)
        
        # TODO: Intégrer l'envoi d'email réel via SMTP
        # Pour l'instant, on log l'email qui devrait être envoyé
        print(f"\n{'='*60}")
        print(f"📧 EMAIL À ENVOYER À: tomgaitano78@mail.com")
        print(f"{'='*60}")
        print(f"Sujet: {title}")
        print(f"Message:\n{message}")
        print(f"{'='*60}\n")
        
        # Configuration SMTP à ajouter dans .env:
        # SMTP_HOST=smtp.gmail.com
        # SMTP_PORT=587
        # SMTP_USER=votre_email@gmail.com
        # SMTP_PASSWORD=votre_mot_de_passe_app
        # ADMIN_EMAIL=tomgaitano78@mail.com
        
        return notification

    @staticmethod
    def get_user_notifications(db: Session, user_id: int) -> List[Notification]:
        return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

    @staticmethod
    def get_admin_notifications(db: Session) -> List[Notification]:
        return db.query(Notification).filter(Notification.user_id == None).order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int):
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            db.commit()
