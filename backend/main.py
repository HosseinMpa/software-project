<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import Base, engine
from routes import auth_routes, movie_routes, booking_routes

# ایجاد جداول دیتابیس
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cinema Reservation System API",
    description="سیستم رزرواسیون بلیط سینما",
    version="1.0.0"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت routes
app.include_router(auth_routes.router)
app.include_router(movie_routes.router)
app.include_router(booking_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "به سیستم رزرواسیون بلیط سینما خوش آمدید",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "cinema-reservation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
=======
from fastapi import FastAPI, Depends, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles 
import uvicorn 
 
from api.routes import auth, bookings, movies 
from api.middlewares.auth_middleware import JWTBearer 
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
>>>>>>> 360738da529f595944e511dab3af6949aa97626e
