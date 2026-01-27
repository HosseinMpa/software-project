from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

BOOKING_FILE = "bookings.json"

class ReservationRequest(BaseModel):
    movieId: int
    time: str
    seats: list[int]

def load_bookings():
    with open(BOOKING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bookings(bookings):
    with open(BOOKING_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=4)

@app.post("/reservations")
def reserve(data: ReservationRequest):
    bookings = load_bookings()

    # چک تداخل صندلی
    for b in bookings:
        if b["movieId"] == data.movieId and b["time"] == data.time:
            for seat in data.seats:
                if seat in b["seats"]:
                    raise HTTPException(
                        status_code=409,
                        detail="Seat already reserved"
                    )

    new_booking = {
        "id": len(bookings) + 1,
        "movieId": data.movieId,
        "time": data.time,
        "seats": data.seats,
        "total": len(data.seats) * 90000,
        "date": "1403/10/10"
    }

    bookings.append(new_booking)
    save_bookings(bookings)

    return {"message": "Reservation successful"}

