from datetime import datetime, date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserRequest(BaseModel):
    email: Annotated[EmailStr, Field(min_length=6, max_length=40)]
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=6)]

class UserAddBase(BaseModel):
    email: EmailStr
    username: str
    data_create_account: Annotated[datetime, Field(datetime.now().replace(tzinfo=None))]
    hashed_password: str

class UserGet(BaseModel):
    id: int
    email: EmailStr
    username: str
    birthday_data: date | None  # Поле может быть необязательным
    data_create_account: datetime

class UserWithHashedPassword(UserGet):
    hashed_password: str