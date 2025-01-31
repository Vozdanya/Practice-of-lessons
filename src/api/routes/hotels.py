from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.schemas import Hotel

router = APIRouter(prefix='/hotels', tags=['Отели'])

examples = [
    {"title": "Сочи Парк Отель", "location": "Континентальный просп., 6, п. г. т. Сириус"},
    {"title": "Sls Dubai Hotel & Residences", "location": "Sls Dubai Hotel & Residences, Бизнес Бей, эмират Дубай"},
]

@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)

        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


# noinspection PyTypeChecker
@router.post("/", name='Добавление нового отеля')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {
        'summary': 'Сочи',
        'value': examples[0]
    },
    '2': {
        'summary': 'Дубай',
        'value': examples[1]
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)

        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}", name='Удаление отеля')
def delete_hotel(hotel_id: int):
    pass

def update_hotel(hotel_id: int, hotel_data: Hotel):
    pass

@router.put('/{hotel_id}', name='Полная вставка данных отеля')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    pass


@router.patch('/{hotel_id}', name='Частичная вставка данных отеля')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    pass
