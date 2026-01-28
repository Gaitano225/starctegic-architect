"""
Test rapide pour vérifier si le signup fonctionne
"""
import requests
import json

url = "http://localhost:8001/api/v1/signup"
data = {
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
}

print(f"Testing signup at: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✓ SUCCESS! User created")
    else:
        print(f"\n✗ FAILED: {response.json()}")
except Exception as e:
    print(f"\n✗ ERROR: {e}")
