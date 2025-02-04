from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from src.schemas.schemas import Hotel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]

HotelDep = Annotated[Hotel, Depends()]