from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.models.hotels import HotelsOrm
from src.repositories.base import RepositoryBase

class HotelsRepository(RepositoryBase):
    model = HotelsOrm

    # get метод
    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
        # Формирование запроса к базе данных
        query = select(self.model)

        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        # Отправляем готовый запрос к базе данных
        result = await self.session.execute(query)
        return result.scalars().all()

    # post метод
    async def add(
            self,
            data: BaseModel
    ):
        # Формирование запроса к базе данных
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model.id)

        # Отправляем готовый запрос к базе данных
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()

    # put метод
    async def edit(
            self,
            data: BaseModel,
            **filter_by: dict
    ) -> None:

        update_data_stmt = update(self.model)

        update_data_stmt = update_data_stmt.filter_by(**filter_by)

        update_data_stmt = update_data_stmt.values(**data.model_dump())

        await self.session.execute(update_data_stmt)




    # delete метод
    async def delete(
            self,
            **filter_by
    ) -> None:
        delete_data_stmt = delete(self.model)

        delete_data_stmt = delete_data_stmt.filter_by(**filter_by)

        await self.session.execute(delete_data_stmt)

