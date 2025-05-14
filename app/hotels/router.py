from datetime import date

from fastapi import APIRouter

from app.exceptions import NotAvailableHotelsException
from app.hotels.dao import HotelsDAO
from app.hotels.models import Hotels
from app.hotels.schemas import SHotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    hotel = await HotelsDAO.find_all(location, date_from, date_to)
    if not hotel:
        raise NotAvailableHotelsException
    return hotel.scalars().all()