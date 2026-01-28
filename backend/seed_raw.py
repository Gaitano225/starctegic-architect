import os
import sys
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.db.session import SessionLocal
from app.core import security

def seed_raw_sql():
    db = SessionLocal()
    try:
        print("Seeding database via Raw SQL...")
        
        # 1. Admin
        pass_admin = security.get_password_hash("Admin2026!")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active)
            VALUES ('admin@strategic.architect', :p, 'Strategic Admin', true, true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": pass_admin})
        
        # 2. Fondateur
        pass_test = security.get_password_hash("Test2026!")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('fondateur@test.com', :p, 'User Fondateur', true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": pass_test})
        
        # 3. Stratege
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('stratege@test.com', :p, 'User Stratege', true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": pass_test})
        
        # 4. Visionnaire
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('visionnaire@test.com', :p, 'User Visionnaire', true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": pass_test})
        
        db.commit()
        print("Users seeded (subscriptions will be created on first login or can be added manually).")
        
    except Exception as e:
        print(f"Raw SQL seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_raw_sql()
