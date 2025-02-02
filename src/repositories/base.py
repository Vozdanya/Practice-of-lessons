from sqlalchemy import select, insert

# Паттерн репозитория
class RepositoryBase:
    # Модель для src/models/...
    model = None

    # Создание экзмепляра класса с новой сессией до начала выполнения методов для эффективного потребления ресурсов компьютера
    def __init__(self, session):
        self.session = session

    # get запрос
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    # post запрос
    async def post_object(self, *args, **kwargs):
        statement = insert(self.model)
        await self.session.execute(statement)
        await self.session.commit()
