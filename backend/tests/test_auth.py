import pytest 
from fastapi.testclient import TestClient 
from main import app 
 
client = TestClient(app) 
 
def test_register_user(): 
    """??? ??????? ?????""" 
    response = client.post("/api/auth/register", json={ 
        "username": "testuser", 
        "email": "test@example.com", 
        "password": "password123", 
        "full_name": "Test User" 
    }) 
    assert response.status_code in [200, 400]  # 200 ???? ?? 400 ??? 
 
def test_login(): 
    """??? ???? ?????""" 
    response = client.post("/api/auth/login", data={ 
        "username": "testuser", 
        "password": "password123" 
    }) 
    assert response.status_code in [200, 401] 
