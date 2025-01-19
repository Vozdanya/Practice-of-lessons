import asyncio
import time

from fastapi import APIRouter, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html

from models.models import Hotel

router = APIRouter(prefix='/hotels')

hotels = [
    {"id": 1, "title": "Sochi", 'name': 'Sochi'},
    {"id": 2, "title": "Дубай", 'name': 'Дубай'},
]


@router.get('/sync/{id}')
def sync_func(id: int):
    print(f'sync.  Started {id}: {time.time():.2f}')
    time.sleep(3)
    print(f'sync.  ended {id}: {time.time():.2f}')

@router.get('/async/{id}')
async def async_func(id: int):
    print(f'async.  Started {id}: {time.time():.2f}')
    await asyncio.sleep(3)
    print(f'async.  ended {id}: {time.time():.2f}')

@router.get("/")
def get_hotels(
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
    return hotels_


@router.post("/")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}
@router.delete("/{hotel_id}")
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

@router.put('/{hotel_id}')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    update_hotel(hotel_id, new_hotel)
    return hotels


@router.patch('/{hotel_id}')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    update_hotel(hotel_id, new_hotel)
    return hotels