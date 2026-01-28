import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('strategic.db')
cursor = conn.cursor()

# Hash bcrypt pré-calculé pour le mot de passe "test123"
# Généré avec: python -c "from passlib.hash import bcrypt; print(bcrypt.hash('test123'))"
bcrypt_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

# Créer l'utilisateur
try:
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, ("stratege@test.com", bcrypt_hash, "Stratege Test", 0, 1))
    
    user_id = cursor.lastrowid
    print(f"✓ Utilisateur créé (ID: {user_id})")
    
    # Créer l'abonnement Stratège
    cursor.execute("""
        INSERT INTO subscriptions (user_id, plan, reports_limit, is_active)
        VALUES (?, ?, ?, ?)
    """, (user_id, "strategist", 10, 1))
    
    conn.commit()
    print("\n" + "="*50)
    print("COMPTE CRÉÉ AVEC SUCCÈS !")
    print("="*50)
    print("Email: stratege@test.com")
    print("Mot de passe: test123")
    print("Plan: Stratège (10 rapports)")
    print("="*50)
    
except sqlite3.IntegrityError as e:
    if "UNIQUE constraint" in str(e):
        print("✓ L'utilisateur existe déjà!")
        print("\nEmail: stratege@test.com")
        print("Mot de passe: test123")
    else:
        print(f"✗ Erreur: {e}")
except Exception as e:
    print(f"✗ Erreur: {e}")
finally:
    conn.close()
