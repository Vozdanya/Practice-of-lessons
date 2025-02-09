from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from sqlalchemy.types import Date, DateTime
from src.database import Base


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    username: Mapped[str] = mapped_column(String(30))
    birthday_data: Mapped[Date | None] = mapped_column(Date, nullable=True)
    data_create_account: Mapped[DateTime] = mapped_column(DateTime)
    hashed_password: Mapped[str] = mapped_column(String(200))