from app.db.base import Base  # Importez tous les modèles ici
from app.db.session import engine
from app.models.user import User
from app.models.project import Project
from app.models.subscription import Subscription
from app.models.meeting import Meeting

def init_db():
    print("Création des tables dans PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()
