import asyncio
from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic.v1 import parse_obj_as

from app.exceptions import NotAvailableHotelsException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
@cache(expire=30)
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    await asyncio.sleep(3)
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