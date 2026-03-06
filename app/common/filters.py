from typing import Optional, TypeVar
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar("T")


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


class SortingParams(BaseModel):
    sort_by: Optional[str] = Field(default=None)
    order: SortOrder = Field(default=SortOrder.ASC)


class FilterParams(PaginationParams, SortingParams):
    search: Optional[str] = Field(default=None)
