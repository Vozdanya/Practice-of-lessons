from pydantic import BaseModel
from sqlalchemy import select, insert

from src.models.hotels import HotelsOrm
from src.repositories.base import RepositoryBase

class HotelsRepository(RepositoryBase):
    model = HotelsOrm

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
            hotel_data: BaseModel
    ):
        # Формирование запроса к базе данных
        add_data_stmt = insert(HotelsOrm).values(**hotel_data.model_dump()).returning(self.model.id)

        # Отправляем готовый запрос к базе данных
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()
