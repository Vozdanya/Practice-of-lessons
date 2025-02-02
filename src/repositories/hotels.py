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
    async def post_object(
            self,
            hotel_data: dict
    ):
        # Формирование запроса к базе данных
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data)

        # Отправляем готовый запрос к базе данных
        await self.session.execute(add_hotel_stmt)

        # Обязательно зафиксировать изменения
        await self.session.commit()

        return {'status': 'OK'}