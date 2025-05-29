from datetime import date

from fastapi import APIRouter

from app.exceptions import (NotAvailableRoomsException,
                            NotRoomsIncorrectDaysException)
from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):

    delta = date_to - date_from
    if delta.days <= 0 or delta.days > 30:
        raise NotRoomsIncorrectDaysException

    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    if not rooms:
        raise NotAvailableRoomsException
    return rooms


