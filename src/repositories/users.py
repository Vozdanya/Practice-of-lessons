from src.models.users import UsersOrm
from src.repositories.base import RepositoryBase
from src.schemas.hotels import HotelAddBase


class UsersRepository(RepositoryBase):
    model = UsersOrm
    schema = HotelAddBase