from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.exceptions import (NotBookingsException, RoomCanNotBeBookedException,
                            RoomCanNotBeBookedIncorrectDaysException)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    bookings =  await BookingDAO.find_all(user_id=user.id)
    if not bookings:
        raise NotBookingsException
    return bookings


@router.post("/")
async def add_booking(
    room_id: int, date_from: date, date_to : date,
    user: Users = Depends(get_current_user)
):

    delta = date_to - date_from
    if delta.days <= 0 or delta.days > 30:
        raise RoomCanNotBeBookedIncorrectDaysException

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBookedException


    booking_dict = parse_obj_as(SBookings, booking).model_dump()

    #send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking_dict



@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
