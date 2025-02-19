from pydantic import BaseModel
from sqlalchemy import insert

from src.models.users import UsersOrm
from src.repositories.base import RepositoryBase

from passlib.context import CryptContext

from src.schemas.users import UserAddBase, UserGet, UserWithHashedPassword
from sqlalchemy import select

class UsersRepository(RepositoryBase):
    model = UsersOrm
    schema = UserGet

    async def add(self, data: BaseModel):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(data.password)

        user_data_dict = data.model_dump(exclude={"password"}, exclude_unset=True)  # Исключаем поле password и добавляем хешированный пароль
        new_user_data = UserAddBase(**user_data_dict, hashed_password=hashed_password)  # Создаем объект UserAddBase

        insert_data_stmt = (insert(self.model)
                            .values(new_user_data
                                    .model_dump()))

        await self.session.execute(insert_data_stmt)

    async def get_user_with_hashed_password(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True) # Для извлечения атрибутов из модели базы данных