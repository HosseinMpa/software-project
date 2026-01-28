# save as test_auth_quick.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    print(f"✅ Health check: {response.status_code} - {response.json()}")

def test_register():
    user_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "password123",
        "confirm_password": "password123",
        "full_name": "کاربر تست"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    print(f"✅ Register: {response.status_code}")
    if response.status_code == 200:
        print(f"   User created: {response.json()}")
    return response

def test_login():
    form_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = client.post("/api/auth/login", data=form_data)
    print(f"✅ Login: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"   Token received: {token[:50]}...")
    return response

if __name__ == "__main__":
    print("🧪 Running Authentication Tests...")
    print("=" * 50)
    
    test_health()
    print()
    
    print("1. Testing registration...")
    register_response = test_register()
    print()
    
    print("2. Testing login...")
    if register_response.status_code in [200, 400]:
        login_response = test_login()
        print()
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("3. Testing protected endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            me_response = client.get("/api/auth/me", headers=headers)
            print(f"✅ Get current user: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"   User info: {me_response.json()}")
    
    print("=" * 50)
    print("✅ All tests completed!")