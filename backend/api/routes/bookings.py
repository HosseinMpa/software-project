from fastapi import APIRouter, HTTPException, Depends 
from pydantic import BaseModel 
from typing import List 
import json 
 
router = APIRouter(tags=["Bookings"]) 
 
class BookingCreate(BaseModel): 
    movie_id: int 
    showtime: str 
    seats: List[int] 
    total_price: int 
 
@router.get("/bookings") 
async def get_bookings(): 
    """?????? ???? ??????""" 
    return [{"message": "Booking endpoint - To be implemented by your teammate"}] 
 
@router.post("/bookings") 
async def create_booking(booking_data: BookingCreate): 
    """????? ???? ????""" 
    return { 
        "message": "Booking created (mock response)", 
        "booking_id": 1, 
        "booking_code": "ABC123" 
    } 
