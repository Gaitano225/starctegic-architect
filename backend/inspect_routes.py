import sys
import os
sys.path.append(os.getcwd())

from app.main import app

for route in app.routes:
    # Check if it has 'path' attribute
    if hasattr(route, "path"):
        print(f"{route.methods} {route.path}")
    elif hasattr(route, "routes"):
        # For nested routers
        for r in route.routes:
             print(f"{r.methods} {r.path}")
