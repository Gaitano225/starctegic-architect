import os
import sys
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.security import get_password_hash

def seed_raw_sql():
    db = SessionLocal()
    try:
        print("Seeding database...")
        
        # Use a consistent password for all test accounts
        pwd = "Password2026!"
        hashed_pwd = get_password_hash(pwd)
        
        # 1. Admin
        print("Creating Admin...")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active)
            VALUES ('admin@strategic.architect', :p, 'Strategic Admin', true, true)
            ON CONFLICT (email) DO UPDATE SET hashed_password = EXCLUDED.hashed_password;
        """), {"p": hashed_pwd})
        
        # 2. Fondateur
        print("Creating Fondateur...")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('fondateur@test.com', :p, 'Utilisateur Fondateur', true)
            ON CONFLICT (email) DO UPDATE SET hashed_password = EXCLUDED.hashed_password;
        """), {"p": hashed_pwd})
        user_2 = db.execute(text("SELECT id FROM users WHERE email='fondateur@test.com'")).fetchone()[0]
        db.execute(text("""
            INSERT INTO subscriptions (user_id, plan, reports_limit, reports_generated, is_active)
            VALUES (:id, 'fondateur', 3, 0, true)
            ON CONFLICT (user_id) DO UPDATE SET plan = EXCLUDED.plan, is_active = EXCLUDED.is_active;
        """), {"id": user_2})
        
        # 3. Stratege
        print("Creating Stratege...")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('stratege@test.com', :p, 'Utilisateur Stratege', true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": hashed_pwd})
        user_3 = db.execute(text("SELECT id FROM users WHERE email='stratege@test.com'")).fetchone()[0]
        db.execute(text("""
            INSERT INTO subscriptions (user_id, plan, reports_limit, reports_generated, is_active)
            VALUES (:id, 'stratege', 10, 0, true)
            ON CONFLICT (user_id) DO UPDATE SET plan = EXCLUDED.plan, is_active = EXCLUDED.is_active;
        """), {"id": user_3})
        
        # 4. Visionnaire
        print("Creating Visionnaire...")
        db.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES ('visionnaire@test.com', :p, 'Utilisateur Visionnaire', true)
            ON CONFLICT (email) DO NOTHING;
        """), {"p": hashed_pwd})
        user_4 = db.execute(text("SELECT id FROM users WHERE email='visionnaire@test.com'")).fetchone()[0]
        db.execute(text("""
            INSERT INTO subscriptions (user_id, plan, reports_limit, reports_generated, is_active)
            VALUES (:id, 'visionnaire', 9999, 0, true)
            ON CONFLICT (user_id) DO UPDATE SET plan = EXCLUDED.plan, is_active = EXCLUDED.is_active;
        """), {"id": user_4})
        
        db.commit()
        print("Seeding completed successfully.")
        print(f"Credentials for all accounts: {pwd}")
        
    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_raw_sql()
