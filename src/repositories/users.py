from pydantic import BaseModel
from sqlalchemy import insert

from src.models.users import UsersOrm
from src.repositories.base import RepositoryBase

from src.schemas.users import UserAddBase, UserGet, UserWithHashedPassword
from sqlalchemy import select

from src.services.auth import authservice


class UsersRepository(RepositoryBase):
    model = UsersOrm
    schema = UserGet

    async def add(self, data: BaseModel):
        # Исключаем поле password
        new_user_data = authservice.replacement_with_hashed_password(data, UserAddBase)

        # Добавляем хэшированный пароль
        insert_data_stmt = (insert(self.model).values(new_user_data.model_dump()))

        await self.session.execute(insert_data_stmt)

    async def get_user_with_hashed_password(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model:
            return UserWithHashedPassword.model_validate(model, from_attributes=True) # Для извлечения атрибутов из модели базы данных

    async def authenticate(self, login: dict, password: str):
        # Находим пользователя из базы
        user_from_base = await self.get_user_with_hashed_password(**login)
        if user_from_base:
            if authservice.authenticate(password, user_from_base.hashed_password):
                return user_from_base