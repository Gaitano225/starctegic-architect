import sys
import os
import traceback

sys.path.append(os.getcwd())

print("--- DIAGNOSTIC START ---")
try:
    print("Importing app.db.base...")
    import app.db.base
    print("Import successful.")
    
    print("Importing SessionLocal...")
    from app.db.session import SessionLocal
    db = SessionLocal()
    
    print("Triggering mapper initialization via query...")
    from app.models.user import User
    db.query(User).first()
    print("SUCCESS: Mapper initialized.")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
    traceback.print_exc()
print("--- DIAGNOSTIC END ---")
