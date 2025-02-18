from datetime import datetime
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

class UserGet(UserRequest):
    id: int