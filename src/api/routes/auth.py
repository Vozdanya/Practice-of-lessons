from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies.dependencies import get_current_user
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequest
from src.services.auth import authservice

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequest):
    async with async_session_maker() as session:
        await UsersRepository(session).add(data)
        await session.commit()
    return {"Status": "OK"}

@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    async with async_session_maker() as session:
        user_exist = await UsersRepository(session).get_user_with_hashed_password(username=form_data.username)
    if not user_exist:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not authservice.verify_password(form_data.password, user_exist.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = authservice.create_access_token({'user_id': user_exist.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(
    user_id: Annotated[int, Depends(get_current_user)]):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return user
