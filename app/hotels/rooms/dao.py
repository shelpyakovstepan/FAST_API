from datetime import date, datetime

from sqlalchemy import and_, func, or_, select

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
            get_rooms = select(Rooms).where(
                Rooms.hotel_id == hotel_id
            )

            rooms = await session.execute(get_rooms)
            rooms = rooms.scalars().all()

            for room in rooms:
                total_cost = (datetime.strptime(str(date_to), "%Y-%m-%d") - datetime.strptime(str(date_from), "%Y-%m-%d")).days * room.price
                rooms_left = 0

                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == room.id,
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
                    booked_rooms, booked_rooms.c.room_id == room.id, isouter=True
                ).where(Rooms.id == room.id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )

                rooms_left_query = await session.execute(get_rooms_left)
                rooms_left += rooms_left_query.scalar()


                room.total_cost = total_cost
                room.rooms_left = rooms_left

            return rooms







