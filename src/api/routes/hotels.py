from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker

from src.repositories.hotels import HotelsRepository

from src.schemas.schemas import Hotel

router = APIRouter(prefix='/hotels', tags=['Отели'])

examples = [
    {"title": "Сочи Парк Отель", "location": "Континентальный просп., 6, п. г. т. Сириус"},
    {"title": "Sls Dubai Hotel & Residences", "location": "Sls Dubai Hotel & Residences, Бизнес Бей, эмират Дубай"},
]

@router.get("/{hotel_id}", name='Получение данных одного отеля')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one(id=hotel_id)

# Возращает пагинацию базу данных с фильтром
@router.get("/", name='Получение данных всех отелей')
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
        await session.commit() # Обязательно зафиксировать изменения
    return {'status': 'OK', 'data': hotel}


@router.put("/{hotel_id}", name='Полное изменение данных отеля')
async def put_hotel(update_data: Hotel, hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=update_data, id=hotel_id)
        await session.commit() # Обязательно зафиксировать изменения
    return {"status": "OK"}


@router.patch("/{hotel_id}", name='Частичное изменение данных отеля')
async def patch_hotel(update_data: Hotel, hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=update_data, exclude_bool=True, id=hotel_id)
        await session.commit() # Обязательно зафиксировать изменения
    return {"status": "OK"}


@router.delete("/{hotel_id}", name='Удаление отеля')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit() # Обязательно зафиксировать изменения
    return {"status": "OK"}

