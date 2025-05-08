from fastapi import FastAPI, Query, Depends
from datetime import date
from typing import Optional
import uvicorn
from pydantic import BaseModel
from app.bookings.router import router as booking_router
from app.users.router import router as user_router

app = FastAPI()

app.include_router(user_router)
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

@app.get("/hotels")
def get_hotels(
    search_hotels: HotelGetArgs = Depends()
) -> list[SHotel]:

    hotels = [
        {
            "address" : "Ул. Ленина, 1, Санкт-Петербург",
            "name" : "Крутой отель",
            "stars" : 5
        }
    ]

    return hotels

@app.post("/booking")
def add_booking(booking: SBooking):
    pass

#if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=800, reload=True)
