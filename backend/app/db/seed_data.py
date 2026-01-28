import sys
import os

# Add the current directory to sys.path to allow importing from 'app'
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base, User, Subscription
from app.models.subscription import PlanType
from app.core import security

def seed_db(db: Session):
    print("Ensuring tables exist...")
    Base.metadata.create_all(bind=engine)
    print("Seeding database...")
    
    # 1. Create Admin Account
    admin_email = "admin@strategic.architect"
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        print(f"Creating admin user: {admin_email}")
        admin_user = User(
            email=admin_email,
            hashed_password=security.get_password_hash("Admin2026!"),
            full_name="Strategic Admin",
            is_superuser=True,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Admin gets a Visionary subscription by default
        admin_sub = Subscription(
            user_id=admin_user.id,
            plan=PlanType.VISIONARY,
            reports_limit=9999
        )
        db.add(admin_sub)
    
    # 2. Test Account - Fondateur
    f_email = "fondateur@test.com"
    if not db.query(User).filter(User.email == f_email).first():
        print(f"Creating fondateur user: {f_email}")
        u = User(
            email=f_email,
            hashed_password=security.get_password_hash("Test2026!"),
            full_name="User Fondateur",
            is_active=True
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        sub = Subscription(user_id=u.id, plan=PlanType.FOUNDER, reports_limit=3)
        db.add(sub)

    # 3. Test Account - Stratège
    s_email = "stratege@test.com"
    if not db.query(User).filter(User.email == s_email).first():
        print(f"Creating stratege user: {s_email}")
        u = User(
            email=s_email,
            hashed_password=security.get_password_hash("Test2026!"),
            full_name="User Stratege",
            is_active=True
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        sub = Subscription(user_id=u.id, plan=PlanType.STRATEGIST, reports_limit=10)
        db.add(sub)

    # 4. Test Account - Visionnaire
    v_email = "visionnaire@test.com"
    if not db.query(User).filter(User.email == v_email).first():
        print(f"Creating visionnaire user: {v_email}")
        u = User(
            email=v_email,
            hashed_password=security.get_password_hash("Test2026!"),
            full_name="User Visionnaire",
            is_active=True
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        sub = Subscription(user_id=u.id, plan=PlanType.VISIONARY, reports_limit=9999)
        db.add(sub)

    db.commit()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
