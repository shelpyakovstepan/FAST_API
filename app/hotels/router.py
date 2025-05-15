from datetime import date
from typing import Type, Any

from fastapi import APIRouter

from app.exceptions import NotAvailableHotelsException
from app.hotels.dao import HotelsDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date):
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