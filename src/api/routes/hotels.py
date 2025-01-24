from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep
from src.models.models import Hotel

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("/")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.post("/", name='Добавление нового отеля')
def create_hotel(
        title: str = Body(),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}
@router.delete("/{hotel_id}", name='Удаление отеля')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return hotels


def update_hotel(hotel_id: int, new_hotel: Hotel):
    global hotels
    for n, hotel in enumerate(hotels):
        if hotel_id == hotel['id']:
            hotels[n] = {"id": hotel_id, "title": new_hotel.title, 'name': new_hotel.name}
            return {"Status": "Ok"}
    return {"error": "all fields are required"}

@router.put('/{hotel_id}', name='Полная вставка данных отеля')
def hotels_put(hotel_id: int, new_hotel: Hotel = Body(openapi_examples={'1': {'summmary': 'Dubai', 'value': hotels[0]},
                                                                        '2': {'summmary': 'sex', 'value': hotels[1]}})):
    update_hotel(hotel_id, new_hotel)
    return hotels


@router.patch('/{hotel_id}', name='Частичная вставка данных отеля')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    update_hotel(hotel_id, new_hotel)
    return hotels