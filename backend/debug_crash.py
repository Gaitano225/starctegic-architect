import sys
import os
import traceback

# Add the current directory to sys.path
sys.path.append(os.getcwd())

print("--- DEBUG START ---")
try:
    print("Attempting to import app.main.app...")
    from app.main import app
    print("SUCCESS: Application imported successfully.")
except NameError as e:
    print(f"FAILED: NameError encountered: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"FAILED: An error of type {type(e).__name__} occurred: {e}")
    traceback.print_exc()
print("--- DEBUG END ---")
