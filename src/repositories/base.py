from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class RepositoryBase:   # Паттерн репозитория
    model = None # Модель для src/models/...

    # Создание экзмепляра класса с новой сессией до начала выполнения методов для эффективного потребления ресурсов компьютера
    def __init__(self, session):
        self.session = session

    # get метод
    async def get_one(self, **filter_by):
        query = (select(self.model) # Формирование запроса к базе данных
                 .filter_by(**filter_by))

        result = await self.session.execute(query) # Отправляем готовый запрос к базе данных

        if result:
            raise HTTPException(status_code=404, detail='Объект не найден')

        return result.scalars().one()

    # get метод
    async def get_all(self, *args, **kwargs):
        query = select(self.model) # Формирование запроса к базе данных

        result = await self.session.execute(query) # Отправляем готовый запрос к базе данных
        return result.scalars().all()

    # post метод
    async def add(self, data: BaseModel):
        insert_data_stmt = (insert(self.model) # Формирование запроса к базе данных
                         .values(**data.model_dump())
                         .returning(self.model.id))

        result = await self.session.execute(insert_data_stmt) # Отправляем готовый запрос к базе данных
        return result.scalars().one()

    # put метод
    async def edit(self, data: BaseModel, exclude_bool: bool = False, **filter_by) -> None:
        update_data_stmt = (update(self.model) # Формирование запроса к базе данных
                            .filter_by(**filter_by)
                            .values(**data.model_dump(exclude_unset=exclude_bool)))

        await self.session.execute(update_data_stmt) # Отправляем готовый запрос к базе данных

    # delete метод
    async def delete(self, **filter_by) -> None:
        delete_data_stmt = (delete(self.model) # Формирование запроса к базе данных
                            .filter_by(**filter_by))

        await self.session.execute(delete_data_stmt) # Отправляем готовый запрос к базе данных
