from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc
from app.common.filters import FilterParams
from typing import Type, TypeVar

T = TypeVar("T")


class BaseRepo:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    def apply_filters(self, query, model: Type[T], params: FilterParams):
        """
        Apply pagination and sorting to a SQLAlchemy query.
        """
        # Sorting
        if params.sort_by and hasattr(model, params.sort_by):
            sort_attr = getattr(model, params.sort_by)
            if params.order == "desc":
                query = query.order_by(desc(sort_attr))
            else:
                query = query.order_by(asc(sort_attr))

        # Pagination
        offset = (params.page - 1) * params.size
        query = query.offset(offset).limit(params.size)

        return query
