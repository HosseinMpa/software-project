import sys 
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
 
from fastapi.testclient import TestClient 
from main import app 
 
client = TestClient(app) 
 
def test_health(): 
    response = client.get("/health") 
    print(f"? Health check: {response.status_code} - {response.json()}") 
 
def test_register(): 
    user_data = { 
        "username": "testuser", 
        "email": "test@example.com", 
        "password": "password123", 
        "confirm_password": "password123", 
        "full_name": "????? ???" 
    } 
 
    response = client.post("/api/auth/register", json=user_data) 
    print(f"? Register: {response.status_code}") 
    if response.status_code == 200: 
        print(f"   User created: {response.json()}") 
    return response 
 
if __name__ == "__main__": 
    print("?? Testing Authentication...") 
    test_health() 
    test_register() 
