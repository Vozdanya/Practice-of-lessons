from src.models.rooms import RoomsOrm
from src.repositories.base import RepositoryBase


class RoomsRepository(RepositoryBase):
    model = RoomsOrm
