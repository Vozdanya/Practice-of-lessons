from sqlalchemy import select

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
            query = (query
                     .filter(HotelsOrm
                             .location
                             .ilike(f"%{location
                                    .strip()}%")))
        if title:
            query = (query
                     .filter(HotelsOrm
                             .title
                             .ilike(f"%{title
                                    .strip()}%")))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        # Отправляем готовый запрос к базе данных
        result = await self.session.execute(query)
        return result.scalars().all()
