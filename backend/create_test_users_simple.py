"""
Script simplifié pour créer 4 utilisateurs de test
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.db.session import engine
from sqlalchemy import text

def create_test_users():
    # Mot de passe hashé pour "Test2026!" (bcrypt)
    # Généré avec: bcrypt.hashpw("Test2026!".encode('utf-8'), bcrypt.gensalt())
    hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5koSj632x/P4W"
    
    users_data = [
        ("fondateur@test.com", "Test Fondateur", "fondateur", 3),
        ("stratege@test.com", "Test Stratège", "stratege", 5),
        ("consultant@test.com", "Test Consultant", "consultant", 7),
        ("visionnaire@test.com", "Test Visionnaire", "visionnaire", 9999)
    ]
    
    with engine.connect() as conn:
        print("🚀 Création des utilisateurs de test...\n")
        
        for email, full_name, plan, reports_limit in users_data:
            # Supprimer l'utilisateur s'il existe
            conn.execute(text("DELETE FROM subscriptions WHERE user_id IN (SELECT id FROM users WHERE email = :email)"), {"email": email})
            conn.execute(text("DELETE FROM users WHERE email = :email"), {"email": email})
            
            # Créer l'utilisateur
            result = conn.execute(
                text("INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser) VALUES (:email, :password, :full_name, true, false) RETURNING id"),
                {"email": email, "password": hashed_password, "full_name": full_name}
            )
            user_id = result.fetchone()[0]
            
            # Créer l'abonnement
            expires_at = (datetime.now() + timedelta(days=30)).isoformat()
            conn.execute(
                text("INSERT INTO subscriptions (user_id, plan, reports_limit, reports_generated, is_active, expires_at) VALUES (:user_id, :plan, :reports_limit, 0, true, :expires_at)"),
                {"user_id": user_id, "plan": plan, "reports_limit": reports_limit, "expires_at": expires_at}
            )
            
            conn.commit()
            
            print(f"✅ {full_name} créé avec succès")
            print(f"   📧 Email: {email}")
            print(f"   🔑 Mot de passe: Test2026!")
            print(f"   📦 Plan: {plan}")
            print(f"   📊 Limite BCT: {reports_limit}")
            print()
        
        print("=" * 60)
        print("🎉 TOUS LES UTILISATEURS DE TEST ONT ÉTÉ CRÉÉS !")
        print("=" * 60)
        print("\n📋 COMPTES DE TEST :\n")
        print("1. fondateur@test.com / Test2026! (Fondateur - 3 BCT/mois)")
        print("2. stratege@test.com / Test2026! (Stratège - 5 BCT/mois)")
        print("3. consultant@test.com / Test2026! (Consultant - 7 BCT/mois)")
        print("4. visionnaire@test.com / Test2026! (Visionnaire - Illimité)")
        print("\n🌐 Connexion: http://localhost:3000/login\n")

if __name__ == "__main__":
    create_test_users()
