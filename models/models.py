from pydantic import BaseModel

class Hotel(BaseModel):
    title: str = 'str'
    name: str = 'str'
