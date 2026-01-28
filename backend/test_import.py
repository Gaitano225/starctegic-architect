import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

try:
    print("Tentative d'importation de app.main...")
    from app.main import app
    print("Importation réussie !")
except NameError as e:
    print(f"CRITICAL NAME ERROR: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
