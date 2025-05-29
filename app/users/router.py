from fastapi import APIRouter, Depends, Response

from app.exceptions import (IncorrectUserEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUsersAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUsersAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuth):
    current_user = await authenticate_user(user_data.email, user_data.password)
    if not current_user:
        raise IncorrectUserEmailOrPasswordException
    access_token = create_access_token({"sub": str(current_user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")

@router.post("/me")
async def get_me(user: Users = Depends(get_current_user)):
    return user
