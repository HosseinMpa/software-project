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