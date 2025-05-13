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
            get_hotel_id = select(Hotels.id).select_from(Hotels).where(
                Hotels.location == location
            )



            get_rooms_id = select(Rooms.id).select_from(Rooms).where(
                Rooms.hotel_id == get_hotel_id.c.id
            )

            rooms = await session.execute(get_rooms_id)
            rooms = rooms.scalars().all()

            rooms_left = 0

            for room_id in rooms:
                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == room_id,
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
                    booked_rooms, booked_rooms.c.room_id == room_id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
                #quantity_rooms_query = select(Rooms.quantity).select_from(Rooms).where(Rooms.id == room_id)
                #booking_rooms_query = select(func.count(booked_rooms.c.room_id)).where(booked_rooms.c.room_id == room_id)
                #quantity_rooms = await session.execute(quantity_rooms_query)
                #booking_rooms = await session.execute(booking_rooms_query)
                #rooms_left += quantity_rooms.scalar() - booking_rooms.scalar()
                rooms_left_query = await session.execute(get_rooms_left)
                rooms_left += rooms_left_query.scalar()


            if rooms_left > 0:
                get_hotel = select(Hotels).where(Hotels.location == location)
                hotel = await session.execute(get_hotel)
                return hotel

            else:
                return None


