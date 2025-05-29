from datetime import date

from sqlalchemy import select, and_, or_, func, insert

from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):

        async with async_session_maker() as session:
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
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )


            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def find_all(
        cls,
        user_id: int
    ):
        async with async_session_maker() as session:
            #get_all_users_bookings = select(Bookings).where(
            #    Bookings.user_id == user_id
            #).cte("get_all_users_bookings")

            #get_all_rooms_parameters = select(
            #    Rooms.image_id,
            #    Rooms.name,
            #    Rooms.description,
            #    Rooms.services
            #).select_from(Rooms).where(
            #    Rooms.id == get_all_users_bookings.c.room_id
            #)
#
            #users_bookings = select(Bookings).join(
            #    get_all_users_bookings, get_all_rooms_parameters, isouter=True).where(
            #    Rooms.id == get_all_users_bookings.c.room_id
            #)



           #users_bookings_result = await session.execute(query)
           #users_bookings_result = users_bookings_result.scalars().all()

           #if not users_bookings_result:
           #    return NotBookingsException

           #return users_bookings_result

            user_bookings = select(Bookings).where(
                Bookings.user_id == user_id
            ).cte("user_bookings")

            query = select(
                user_bookings.c.id,
                user_bookings.c.room_id,
                user_bookings.c.user_id,
                user_bookings.c.date_from,
                user_bookings.c.date_to,
                user_bookings.c.price,
                user_bookings.c.total_cost,
                user_bookings.c.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).select_from(
                user_bookings.join(
                    Rooms,
                    Rooms.id == user_bookings.c.room_id,
                    isouter=True
                )
            ).order_by(user_bookings.c.date_from)

            result = await session.execute(query)
            bookings = result.mappings().all()

            return bookings

