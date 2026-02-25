from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db
