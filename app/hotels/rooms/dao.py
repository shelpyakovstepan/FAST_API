from datetime import date

from sqlalchemy import select, and_, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            get_rooms_id = select(Rooms).select_from(Rooms).where(
                Rooms.hotel_id == hotel_id
            ).cte("get_rooms_id")

            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == get_rooms_id.c.id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_to <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),

                    )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == get_rooms_id.c.id, isouter=True
            ).where(Rooms.id == get_rooms_id.c.id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                rooms = select(Rooms).where(id == get_rooms_id.c.id)
                rooms = await session.execute(rooms)
                return rooms
            else:
                return None


