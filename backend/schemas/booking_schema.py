from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SeatSelection(BaseModel):
    seat_id: int
    seat_number: str

class BookingCreate(BaseModel):
    showtime_id: int
    seat_ids: List[int]
    payment_method: str = "cash"

class BookingResponse(BaseModel):
    id: int
    user_id: int
    showtime_id: int
    seat_numbers: str
    total_price: float
    status: BookingStatus
    booking_code: str
    movie_title: Optional[str] = None
    showtime: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    payment_status: Optional[str] = None