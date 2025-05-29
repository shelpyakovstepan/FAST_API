from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize("user_id,room_id,date_from,date_to", [
    (2, 2, "2023-07-10", "2023-07-24")
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")
    new_booking = await BookingDAO.add(user_id, room_id, date_from, date_to)

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


@pytest.mark.parametrize("user_id,room_id,date_from,date_to", [
    (1, 4, "2030-09-08", "2030-09-18"),
    (2, 5, "2030-09-08", "2030-09-18")
])
async def test_add_get_and_delete_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    new_booking = await BookingDAO.add(user_id, room_id, date_from, date_to)

    new_booking= await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None

    await BookingDAO.delete(id=new_booking.id)

    delete_booking = await BookingDAO.find_by_id(new_booking.id)

    assert delete_booking is None