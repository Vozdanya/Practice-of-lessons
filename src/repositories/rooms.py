from src.models.rooms import RoomsOrm
from src.repositories.base import RepositoryBase


class HotelsRepository(RepositoryBase):
    model = RoomsOrm