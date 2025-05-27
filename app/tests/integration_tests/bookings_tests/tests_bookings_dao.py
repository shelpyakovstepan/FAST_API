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

    new_booking = BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None