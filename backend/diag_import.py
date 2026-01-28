import sys
import os
import traceback

# Add current path
sys.path.append(os.getcwd())

print("--- DIAGNOSTIC DÉBUT ---")
try:
    print("Tentative d'importation de app.main.app...")
    from app.main import app
    print("Importation réussie de l'application !")
except NameError as e:
    print(f"FAILED: NameError: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
    traceback.print_exc()
print("--- DIAGNOSTIC FIN ---")
