from datetime import date
from sqlalchemy import func, and_, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):

        async with async_session_maker() as session:
            get_hotels = select(Hotels).where(
                Hotels.location == location
            )

            hotels = await session.execute(get_hotels)
            hotels = hotels.scalars().all()


            for hotel in hotels:
                rooms_left = 0
                get_rooms = select(Rooms).where(
                    Rooms.hotel_id == hotel.id
                )

                rooms = await session.execute(get_rooms)
                rooms = rooms.scalars().all()

                for room in rooms:
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


                if rooms_left == 0:
                    hotels.remove(hotel)
                hotel.rooms_left = rooms_left


            return hotels


