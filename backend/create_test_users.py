"""
Script pour créer 4 utilisateurs de test (un par forfait)
À exécuter une seule fois pour peupler la base de données
"""
import sys
import os
from datetime import datetime, timedelta

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.subscription import Subscription, PlanType
from app.core.security import get_password_hash

def create_test_users():
    db = SessionLocal()
    
    # Mot de passe par défaut pour tous les comptes de test
    default_password = "Test2026!"
    
    test_users = [
        {
            "email": "fondateur@test.com",
            "full_name": "Test Fondateur",
            "plan": "fondateur",
            "reports_limit": 3
        },
        {
            "email": "stratege@test.com",
            "full_name": "Test Stratège",
            "plan": "stratege",
            "reports_limit": 5
        },
        {
            "email": "consultant@test.com",
            "full_name": "Test Consultant",
            "plan": "consultant",
            "reports_limit": 7
        },
        {
            "email": "visionnaire@test.com",
            "full_name": "Test Visionnaire",
            "plan": "visionnaire",
            "reports_limit": 9999
        }
    ]
    
    print("🚀 Création des utilisateurs de test...\n")
    
    for user_data in test_users:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        
        if existing_user:
            print(f"⚠️  {user_data['email']} existe déjà, suppression et recréation...")
            # Supprimer l'abonnement existant
            db.query(Subscription).filter(Subscription.user_id == existing_user.id).delete()
            # Supprimer l'utilisateur
            db.delete(existing_user)
            db.commit()
        
        # Créer l'utilisateur
        user = User(
            email=user_data["email"],
            hashed_password=get_password_hash(default_password),
            full_name=user_data["full_name"],
            is_active=True,
            is_superuser=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Créer l'abonnement
        subscription = Subscription(
            user_id=user.id,
            plan=user_data["plan"],
            reports_limit=user_data["reports_limit"],
            reports_generated=0,
            is_active=True,
            expires_at=datetime.now() + timedelta(days=30)
        )
        db.add(subscription)
        db.commit()
        
        print(f"✅ {user_data['full_name']} créé avec succès")
        print(f"   📧 Email: {user_data['email']}")
        print(f"   🔑 Mot de passe: {default_password}")
        print(f"   📦 Plan: {user_data['plan']}")
        print(f"   📊 Limite BCT: {user_data['reports_limit']}")
        print()
    
    db.close()
    
    print("=" * 60)
    print("🎉 TOUS LES UTILISATEURS DE TEST ONT ÉTÉ CRÉÉS !")
    print("=" * 60)
    print("\n📋 RÉCAPITULATIF DES COMPTES :\n")
    print("1. FONDATEUR")
    print("   Email: fondateur@test.com")
    print("   Mot de passe: Test2026!")
    print("   Plan: Fondateur (3 BCT/mois)")
    print()
    print("2. STRATÈGE")
    print("   Email: stratege@test.com")
    print("   Mot de passe: Test2026!")
    print("   Plan: Stratège (5 BCT/mois)")
    print()
    print("3. CONSULTANT")
    print("   Email: consultant@test.com")
    print("   Mot de passe: Test2026!")
    print("   Plan: Consultant (7 BCT/mois)")
    print()
    print("4. VISIONNAIRE")
    print("   Email: visionnaire@test.com")
    print("   Mot de passe: Test2026!")
    print("   Plan: Visionnaire (BCT illimités)")
    print()
    print("🌐 Connectez-vous sur http://localhost:3000/login")
    print()

if __name__ == "__main__":
    create_test_users()
