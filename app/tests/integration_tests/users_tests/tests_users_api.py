import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("pes@kot.com", "pesokot", 200),
    ("pes@kot.com", "pesokot", 409),
    ("kot@pes.com", "kotopes", 200),
    ("step3210shelpyakov@gmail.com", "fff", 409),
    ("abcde", "kotopes", 422)

])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("step3210shelpyakov@gmail.com", "kolobok", 200),
    ("user@example.com", "parol", 200),
    ("step3210shelpyakov@gmail.com", "fff", 401),
    ("abcde", "kotopes", 422),
    ("step@gmail.com", "kolobok", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code

