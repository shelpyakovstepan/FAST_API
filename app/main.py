from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as booking_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as hotels_room_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.users.router import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(user_router)
app.include_router(hotels_router)
app.include_router(hotels_room_router)
app.include_router(booking_router)

app.include_router(pages_router)

app.include_router(images_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

#origins = [
#    домен
#]
#
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "PUT"],
#    allow_headers=["Set-Cookie", "Content-Type", "Authorization", "Access-Control-Allow-Headers",
#                   "Access-Control-Allow-Origin"],
#)


#команды для запуска

#celery -A app.tasks.celery_app:celery worker --loglevel=INFO --pool=solo

#uvicorn app.main:app --reload

#celery -A app.tasks.celery_app:celery flower

#pytest -v -s app/tests/integration_tests/hotels_tests/tests_bookings_api.py