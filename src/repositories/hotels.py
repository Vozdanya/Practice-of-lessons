from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import RepositoryBase
from src.schemas.schemas import Hotel_Add_ID


class HotelsRepository(RepositoryBase):
    model = HotelsOrm
    schema = Hotel_Add_ID

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
        objects = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in objects]
