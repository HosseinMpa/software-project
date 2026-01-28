# simple_auth.py - برای تست سریع Authentication
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlite3
import os

app = FastAPI(title="Simple Auth API")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database setup
def init_db():
    conn = sqlite3.connect('simple_auth.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Pydantic models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

# JWT settings
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Database initialized")

@app.post("/register", response_model=UserResponse)
async def register(user: UserRegister):
    conn = sqlite3.connect('simple_auth.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", 
                   (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Insert user
    cursor.execute('''
        INSERT INTO users (username, email, full_name, hashed_password)
        VALUES (?, ?, ?, ?)
    ''', (user.username, user.email, user.full_name, hashed_password))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name
    }

@app.post("/login")
async def login(user: UserLogin):
    conn = sqlite3.connect('simple_auth.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, hashed_password 
        FROM users WHERE username = ?
    ''', (user.username,))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id, username, email, full_name, hashed_password = user_data
    
    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(
        data={"sub": username, "user_id": user_id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username
    }

@app.get("/users/me")
async def read_users_me(token: str = Depends(lambda: "")):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {"user_id": user_id, "username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def root():
    return {"message": "Simple Auth API", "endpoints": ["/register", "/login", "/users/me"]}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Simple Auth API starting...")
    print("📌 Endpoints:")
    print("  - POST /register")
    print("  - POST /login") 
    print("  - GET  /users/me")
    print("\nOpen: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)