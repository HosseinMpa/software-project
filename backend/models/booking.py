from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text 
from sqlalchemy.sql import func 
from database.database import Base 
 
class Booking(Base): 
    __tablename__ = "bookings" 
 
    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    movie_id = Column(Integer, nullable=False) 
    showtime = Column(String(10))  # Format: "14:00" 
    seats = Column(Text)  # JSON string of seat numbers 
    total_price = Column(Integer, nullable=False) 
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled 
    booking_code = Column(String(20), unique=True, index=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
 
    def __repr__(self): 
        return f"<Booking(id={self.id}, booking_code={self.booking_code})>" 
