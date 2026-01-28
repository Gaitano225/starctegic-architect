"""
Script simple pour créer les comptes de test
"""
import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from app.core.security import get_password_hash

# Connexion à la base de données
DATABASE_URL = "sqlite:///./strategic.db"
engine = create_engine(DATABASE_URL)

# Mot de passe simple pour tous les comptes de test
password = "test123"
hashed = get_password_hash(password)

users = [
    ("admin@strategic.com", "Strategic Admin", True),
    ("fondateur@test.com", "User Fondateur", False),
    ("stratege@test.com", "User Stratège", False),
    ("visionnaire@test.com", "User Visionnaire", False),
]

with engine.connect() as conn:
    # Créer les utilisateurs
    for email, full_name, is_super in users:
        try:
            result = conn.execute(text(
                "INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active) "
                "VALUES (:email, :pwd, :name, :super, 1)"
            ), {"email": email, "pwd": hashed, "name": full_name, "super": 1 if is_super else 0})
            conn.commit()
            print(f"✓ Créé: {email}")
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print(f"- Existe déjà: {email}")
            else:
                print(f"✗ Erreur pour {email}: {e}")
    
    # Créer les abonnements
    plans = [
        ("admin@strategic.com", "visionary", 9999),
        ("fondateur@test.com", "founder", 3),
        ("stratege@test.com", "strategist", 10),
        ("visionnaire@test.com", "visionary", 9999),
    ]
    
    for email, plan, limit in plans:
        try:
            conn.execute(text(
                "INSERT INTO subscriptions (user_id, plan, reports_limit, is_active) "
                "SELECT id, :plan, :limit, 1 FROM users WHERE email = :email"
            ), {"email": email, "plan": plan, "limit": limit})
            conn.commit()
            print(f"✓ Abonnement {plan} pour {email}")
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print(f"- Abonnement existe déjà pour {email}")
            else:
                print(f"✗ Erreur abonnement {email}: {e}")

print("\n" + "="*50)
print("COMPTES DE TEST CRÉÉS")
print("="*50)
print("Email: admin@strategic.com")
print("Email: fondateur@test.com")
print("Email: stratege@test.com")
print("Email: visionnaire@test.com")
print(f"\nMot de passe pour tous: {password}")
print("="*50)
