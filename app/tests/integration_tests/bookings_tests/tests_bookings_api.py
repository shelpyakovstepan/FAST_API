import pytest
from httpx import AsyncClient

from app.tests.conftest import authenticated_ac


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms, status_code",[
    (4, "2030-05-01", "2030-05-02", 10, 200),
    (4, "2030-05-01", "2030-05-02", 11, 200),
    (4, "2030-05-01", "2030-05-02", 12, 200),
    (4, "2030-05-01", "2030-05-02", 13, 200),
    (4, "2030-05-01", "2030-05-02", 14, 200),
    (4, "2030-05-01", "2030-05-02", 15, 200),
    (4, "2030-05-01", "2030-05-02", 16, 200),
    (4, "2030-05-01", "2030-05-02", 17, 200),
    (4, "2030-05-01", "2030-05-02", 17, 409),
])
async def test_add_and_get_bookings(room_id, date_from, date_to,
                                    booked_rooms,
                                    status_code,
                                    authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/bookings/", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms



async def test_get_and_delete_bookings(authenticated_ac: AsyncClient):
    bookings = await authenticated_ac.get("/bookings")

    for booking in bookings.json():
        booking_id = booking["id"]
        await authenticated_ac.delete(f"/bookings/{booking_id}")

    response = await authenticated_ac.get("/bookings")

    assert response.status_code == 409


