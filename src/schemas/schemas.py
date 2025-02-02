from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: Annotated[str | None, Query(None)]
    location: Annotated[str | None, Query(None)]

