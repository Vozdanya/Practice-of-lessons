from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

# Создание асинхронного движка
engine = create_async_engine(settings.DB_URL)

# async_sessionmaker: Это фабрика, которая создает асинхронные сессии.

# bind=engine: Указывает, что сессии будут использовать созданный ранее движок (engine).

# expire_on_commit=False: Отключает автоматическое "истечение" (expire) объектов после коммита.
# Это полезно, чтобы объекты оставались доступными для использования после завершения транзакции.

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# Для наследования в src/models/...
class Base(DeclarativeBase):
    pass