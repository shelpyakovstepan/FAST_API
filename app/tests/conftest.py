import json
from datetime import datetime

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")


    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)) as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)) as ac:
        await ac.post("/auth/login", json={
            "email": "user@example.com",
            "password": "parol"
        })
        assert ac.cookies["access_token"]
        yield ac



#@pytest.fixture(scope="session")
#def event_loop():
#    policy = asyncio.get_event_loop_policy()
#    loop = policy.new_event_loop()
#    yield loop
#    loop.close()
