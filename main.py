from fastapi import FastAPI, Query
from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from models import Hotel

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", 'name': 'Sochi'},
    {"id": 2, "title": "Дубай", 'name': 'Дубай'},
]


@app.get("/hotels")
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


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}
@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return hotels

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
def update_hotel(hotel_id: int, new_hotel: Hotel):
    global hotels
    for n, hotel in enumerate(hotels):
        if hotel_id == hotel['id']:
            hotels[n] = {"id": hotel_id, "title": new_hotel.title, 'name': new_hotel.name}
            return {"Status": "Ok"}
    return {"error": "all fields are required"}

@app.put('/hotels/{hotel_id}')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    update_hotel(hotel_id, new_hotel)
    return hotels


@app.patch('/hotels/{hotel_id}')
def hotels_put(hotel_id: int, new_hotel: Hotel):
    update_hotel(hotel_id, new_hotel)
    return hotels

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)