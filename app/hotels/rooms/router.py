from datetime import date

from app.exceptions import NotAvailableRoomsException
from app.hotels.rooms.dao import RoomsDAO
from fastapi import APIRouter

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    if not rooms:
        raise NotAvailableRoomsException
    return rooms


