<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    seat_ids = Column(Text)  # JSON string of seat IDs ["1", "2", "3"]
    seat_numbers = Column(Text)  # Display string "A1, A2, A3"
    total_price = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    payment_method = Column(String(50))
    payment_status = Column(String(50), default="unpaid")
    booking_code = Column(String(20), unique=True, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    showtime = relationship("Showtime", back_populates="bookings")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "showtime_id": self.showtime_id,
            "seat_numbers": self.seat_numbers,
            "total_price": self.total_price,
            "status": self.status.value,
            "booking_code": self.booking_code,
            "movie_title": self.showtime.movie.title if self.showtime and self.showtime.movie else None,
            "showtime": self.showtime.start_time.isoformat() if self.showtime else None,
            "created_at": self.created_at.isoformat()
        }
=======
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
>>>>>>> 360738da529f595944e511dab3af6949aa97626e
