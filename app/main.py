from fastapi import FastAPI, Query, Depends
from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.bookings.router import router as booking_router
from app.users.router import router as user_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as hotels_room_router
app = FastAPI()

app.include_router(user_router)
app.include_router(hotels_router)
app.include_router(hotels_room_router)
app.include_router(booking_router)

class SHotel(BaseModel):
    address: str
    name: str
    stars: int

class SBooking(BaseModel):
    room_id : int
    date_from: date
    date_to: date

class HotelGetArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars

