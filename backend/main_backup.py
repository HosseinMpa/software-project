from fastapi import FastAPI, Depends, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles 
import uvicorn 
 
from api.routes import auth, bookings, movies\nfrom api.middlewares.auth_middleware import JWTBearer 
from database.database import engine, Base 
from config.settings import settings 
 
# Create tables 
Base.metadata.create_all(bind=engine) 
 
app = FastAPI( 
    title="Cinema Reservation API", 
    description="Backend for Cinema Ticket Booking System", 
    version="1.0.0" 
) 
 
# CORS 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 
 
# Include routers 
app.include_router(auth.router, prefix="/api") 
app.include_router(bookings.router, prefix="/api") 
app.include_router(movies.router, prefix="/api") 
 
@app.get("/") 
async def root(): 
    return {"message": "?? Cinema Reservation API", "version": "1.0.0"} 
 
@app.get("/health") 
async def health(): 
    return {"status": "healthy"} 
 
if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000) 
