from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()

print(f"Total users: {len(users)}")
for u in users:
    print(f"ID: {u.id} | Email: {u.email} | Active: {u.is_active} | Admin: {u.is_superuser}")

db.close()
