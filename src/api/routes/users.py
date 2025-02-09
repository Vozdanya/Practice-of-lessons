from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAddBase

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)

    user_data_dict = data.model_dump(exclude={"password"}, exclude_unset=True)  # Исключаем поле password и добавляем хешированный пароль
    new_user_data = UserAddBase(**user_data_dict, hashed_password=hashed_password) # Создаем объект UserAddBase
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"Status": "OK"}