 
<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from database import Base
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    genre = Column(String(100))
    duration = Column(Integer)  # مدت به دقیقه
    director = Column(String(100))
    cast = Column(Text)  # بازیگران
    release_date = Column(DateTime)
    rating = Column(Float)
    poster_url = Column(String(500))
    trailer_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "duration": self.duration,
            "director": self.director,
            "cast": self.cast,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "rating": self.rating,
            "poster_url": self.poster_url,
            "trailer_url": self.trailer_url
        }
=======
>>>>>>> 360738da529f595944e511dab3af6949aa97626e
