import sqlite3
import hashlib

# Connexion à la base de données
conn = sqlite3.connect('strategic.db')
cursor = conn.cursor()

# Créer un hash simple (SHA256 au lieu de bcrypt pour éviter les problèmes)
# Note: En production, utiliser bcrypt, mais pour le debug on utilise SHA256
password = "test123"
hashed = hashlib.sha256(password.encode()).hexdigest()

# Insérer un utilisateur de test
try:
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, ("demo@test.com", f"$2b$12${hashed}", "Demo User", 0, 1))
    
    user_id = cursor.lastrowid
    
    # Créer un abonnement
    cursor.execute("""
        INSERT INTO subscriptions (user_id, plan, reports_limit, is_active)
        VALUES (?, ?, ?, ?)
    """, (user_id, "founder", 999, 1))
    
    conn.commit()
    print("✓ Utilisateur créé avec succès!")
    print(f"Email: demo@test.com")
    print(f"Mot de passe: {password}")
    print(f"\nIMPORTANT: Ce compte utilise un hash temporaire.")
    print("Pour te connecter, utilise le mode 'invité' du questionnaire.")
    
except sqlite3.IntegrityError:
    print("✗ L'utilisateur existe déjà")
except Exception as e:
    print(f"✗ Erreur: {e}")
finally:
    conn.close()
