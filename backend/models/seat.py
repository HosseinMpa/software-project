from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class SeatType(enum.Enum):
    REGULAR = "regular"
    VIP = "vip"
    COUPLE = "couple"

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)  # مانند "A1", "B5"
    seat_type = Column(Enum(SeatType), default=SeatType.REGULAR)
    is_available = Column(Boolean, default=True)
    row = Column(String(2))  # ردیف: A, B, C, ...
    column = Column(Integer)  # ستون: 1, 2, 3, ...
    
    # Relationships
    showtime = relationship("Showtime")
    
    def to_dict(self):
        return {
            "id": self.id,
            "seat_number": self.seat_number,
            "seat_type": self.seat_type.value,
            "is_available": self.is_available,
            "row": self.row,
            "column": self.column
        }