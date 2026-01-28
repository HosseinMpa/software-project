from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Showtime(Base):
    __tablename__ = "showtimes"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_name = Column(String(50))  # نام سالن
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    available_seats = Column(Integer, default=100)
    total_seats = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    movie = relationship("Movie")
    bookings = relationship("Booking", back_populates="showtime")
    
    def to_dict(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "movie_title": self.movie.title if self.movie else None,
            "hall_name": self.hall_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "price": self.price,
            "available_seats": self.available_seats,
            "total_seats": self.total_seats
        }