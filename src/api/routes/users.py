from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from fastapi.security import OAuth2PasswordBearer

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequest, UserGet

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.post("/register")
async def register_user(data: UserRequest):
    async with async_session_maker() as session:
        await UsersRepository(session).add(data)
        await session.commit()
    return {"Status": "OK"}

@router.get('/auth')
async def auth_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}