from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
import uuid
import json

from models.booking import Booking, BookingStatus
from models.showtime import Showtime
from models.seat import Seat

class BookingService:
    
    @staticmethod
    def create_booking(db: Session, user_id: int, showtime_id: int, 
                      seat_ids: list, payment_method: str) -> Booking:
        """ایجاد یک رزرو جدید"""
        
        # بررسی وجود سانس
        showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
        if not showtime:
            raise ValueError("سانس مورد نظر یافت نشد")
        
        # بررسی تاریخ سانس (نباید گذشته باشد)
        if showtime.start_time < datetime.utcnow():
            raise ValueError("زمان سانس گذشته است")
        
        # بررسی تعداد صندلی‌های درخواستی
        if len(seat_ids) > 6:  # حداکثر ۶ صندلی
            raise ValueError("حداکثر می‌توان ۶ صندلی رزرو کرد")
        
        # بررسی موجودی صندلی‌ها
        seats = db.query(Seat).filter(
            Seat.id.in_(seat_ids),
            Seat.showtime_id == showtime_id,
            Seat.is_available == True
        ).all()
        
        if len(seats) != len(seat_ids):
            raise ValueError("برخی صندلی‌ها در دسترس نیستند")
        
        # محاسبه قیمت کل
        total_price = sum(seat.showtime.price for seat in seats)
        
        # تولید کد رزرو
        booking_code = f"BK{uuid.uuid4().hex[:8].upper()}"
        
        # ایجاد رزرو
        booking = Booking(
            user_id=user_id,
            showtime_id=showtime_id,
            seat_ids=json.dumps(seat_ids),
            seat_numbers=", ".join([seat.seat_number for seat in seats]),
            total_price=total_price,
            status=BookingStatus.CONFIRMED,
            payment_method=payment_method,
            payment_status="paid" if payment_method == "online" else "pending",
            booking_code=booking_code
        )
        
        db.add(booking)
        
        # رزرو صندلی‌ها
        for seat in seats:
            seat.is_available = False
        
        # به‌روزرسانی تعداد صندلی‌های خالی
        showtime.available_seats -= len(seat_ids)
        
        db.commit()
        db.refresh(booking)
        
        return booking
    
    @staticmethod
    def get_user_bookings(db: Session, user_id: int):
        """دریافت رزروهای کاربر"""
        bookings = db.query(Booking).filter(
            Booking.user_id == user_id
        ).order_by(Booking.created_at.desc()).all()
        
        return bookings
    
    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user_id: int):
        """لغو رزرو"""
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_id == user_id
        ).first()
        
        if not booking:
            raise ValueError("رزرو یافت نشد")
        
        if booking.status == BookingStatus.CANCELLED:
            raise ValueError("رزرو قبلاً لغو شده است")
        
        booking.status = BookingStatus.CANCELLED
        booking.payment_status = "refunded"
        
        # آزاد کردن صندلی‌ها
        seat_ids = json.loads(booking.seat_ids)
        db.query(Seat).filter(Seat.id.in_(seat_ids)).update(
            {"is_available": True}
        )
        
        # به‌روزرسانی تعداد صندلی‌های خالی
        showtime = booking.showtime
        showtime.available_seats += len(seat_ids)
        
        db.commit()
        
        return booking
