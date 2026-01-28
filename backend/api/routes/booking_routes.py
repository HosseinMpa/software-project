from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from database import get_db
from models.booking import Booking, BookingStatus
from models.showtime import Showtime
from models.seat import Seat
from schemas.booking_schema import (
    BookingCreate, BookingResponse, 
    SeatSelection, BookingUpdate
)
from services.booking_service import BookingService
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.get("/", response_model=List[BookingResponse])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت تمام رزروهای کاربر"""
    bookings = BookingService.get_user_bookings(db, current_user.id)
    return bookings

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ایجاد رزرو جدید"""
    try:
        booking = BookingService.create_booking(
            db=db,
            user_id=current_user.id,
            showtime_id=booking_data.showtime_id,
            seat_ids=booking_data.seat_ids,
            payment_method=booking_data.payment_method
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="خطا در ایجاد رزرو")

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت اطلاعات یک رزرو خاص"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="رزرو یافت نشد")
    
    return booking

@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """لغو رزرو"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="رزرو یافت نشد")
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="رزرو قبلاً لغو شده است")
    
    # فقط رزروهای pending یا confirmed قابل لغو هستند
    if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="این رزرو قابل لغو نیست")
    
    booking.status = BookingStatus.CANCELLED
    
    # آزاد کردن صندلی‌ها
    seat_ids = eval(booking.seat_ids)
    db.query(Seat).filter(Seat.id.in_(seat_ids)).update(
        {"is_available": True}
    )
    
    db.commit()
    db.refresh(booking)
    
    return booking

@router.get("/showtime/{showtime_id}/seats")
def get_available_seats(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    """دریافت صندلی‌های قابل رزرو برای یک سانس"""
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="سانس یافت نشد")
    
    seats = db.query(Seat).filter(
        Seat.showtime_id == showtime_id,
        Seat.is_available == True
    ).all()
    
    return {
        "showtime": showtime.to_dict(),
        "available_seats": [seat.to_dict() for seat in seats],
        "total_seats": showtime.total_seats,
        "available_count": showtime.available_seats
    }