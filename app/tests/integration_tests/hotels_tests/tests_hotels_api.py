import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Республика Коми, Сыктывкар, Коммунистическая улица, 67", "2030-09-10", "2030-09-11", 200),
    ("Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20", "2030-09-01", "2030-08-01", 400),
    ("Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20", "2030-09-01", "2030-09-01", 400),
    ("Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20", "2030-09-01", "2030-10-11", 400)
])
async def test_get_hotels_by_location(location, date_from, date_to, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/{location}", params={
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code


