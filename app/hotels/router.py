from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import (NotAvailableHotelsException,
                            NotHotelsIncorrectDaysException)
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
#@cache(expire=30)
async def get_hotels_by_location(location: str, date_from: date, date_to: date) -> list[SHotels]:

    delta = date_to - date_from
    if delta.days <= 0 or delta.days > 30:
        raise NotHotelsIncorrectDaysException

    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    if not hotels:
        raise NotAvailableHotelsException
    return hotels

@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        return NotAvailableHotelsException
    return hotel