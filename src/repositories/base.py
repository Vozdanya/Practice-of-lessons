from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

class RepositoryBase:   # Паттерн репозитория
    model = None # Модель для src/models/...
    schema: BaseModel = None # Схема для src/schemas/...

    # Создание экзмепляра класса с новой сессией до начала выполнения методов для эффективного потребления ресурсов компьютера
    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by): # get метод
        query = (select(self.model) # Формирование запроса к базе данных
                 .filter_by(**filter_by))
        result = await self.session.execute(query) # Отправляем готовый запрос к базе данных
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj, from_attributes=True) # Для извлечения атрибутов из модели базы данных

    async def get_all(self, *args, **kwargs): # get метод
        query = select(self.model) # Формирование запроса к базе данных
        result = await self.session.execute(query) # Отправляем готовый запрос к базе данных
        objects = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in objects] # Для извлечения атрибутов из модели базы данных

    async def add(self, data: BaseModel): # post метод
        insert_data_stmt = (insert(self.model) # Формирование запроса к базе данных
                         .values(**data.model_dump())
                         .returning(self.model.id))
        result = await self.session.execute(insert_data_stmt) # Отправляем готовый запрос к базе данных
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_bool: bool = False, **filter_by) -> None: # put метод
        update_data_stmt = (update(self.model) # Формирование запроса к базе данных
                            .filter_by(**filter_by)
                            .values(**data.model_dump(exclude_unset=exclude_bool)))
        await self.session.execute(update_data_stmt) # Отправляем готовый запрос к базе данных

    async def delete(self, **filter_by) -> None: # delete метод
        delete_data_stmt = (delete(self.model) # Формирование запроса к базе данных
                            .filter_by(**filter_by))
        await self.session.execute(delete_data_stmt) # Отправляем готовый запрос к базе данных
