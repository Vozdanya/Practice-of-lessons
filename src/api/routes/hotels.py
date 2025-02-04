from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, HotelDep
from src.database import async_session_maker

from src.repositories.hotels import HotelsRepository

from src.schemas.schemas import Hotel



router = APIRouter(prefix='/hotels', tags=['Отели'])

examples = [
    {"title": "Сочи Парк Отель", "location": "Континентальный просп., 6, п. г. т. Сириус"},
    {"title": "Sls Dubai Hotel & Residences", "location": "Sls Dubai Hotel & Residences, Бизнес Бей, эмират Дубай"},
]

# Показывает пагинацию базу данных с фильтром
@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='ИМЯ'),
        location: str | None = Query(None, description='АДРЕС')
):


    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

# Добавляет новый отель в базу данных
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
        hotel = await HotelsRepository(session).add(hotel_data)
        # Обязательно зафиксировать изменения
        await session.commit()

    return {'status': 'OK', 'data': hotel}

@router.put("/{hotel_id}")
async def edit_hotel(update_id: int, update_data: Hotel, change_data: HotelDep):
    change_data = {key: value for key, value in change_data.model_dump().items() if value is not None}

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=update_data, id=update_id, **change_data)
        # Обязательно зафиксировать изменения
        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        # Обязательно зафиксировать изменения
        await session.commit()
    return {"status": "OK"}

