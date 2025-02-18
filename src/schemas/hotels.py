from typing import Annotated
from fastapi import Query
from pydantic import BaseModel

class HotelRequest(BaseModel):
    title: Annotated[str | None, Query(None)]
    location: Annotated[str | None, Query(None)]

class HotelGet(HotelRequest):
    id: int

