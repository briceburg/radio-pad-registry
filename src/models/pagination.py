import math
from typing import TypeVar

from pydantic import BaseModel, model_validator

T = TypeVar("T")


class PaginatedList[T](BaseModel):
    items: list[T]
    total: int
    page: int
    per_page: int

    # Derived fields populated post-validation
    pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    next_page: int | None = None
    prev_page: int | None = None

    @model_validator(mode="after")
    def _compute(self) -> "PaginatedList[T]":
        self.pages = math.ceil(self.total / self.per_page) if self.per_page else 0
        self.has_next = self.page < self.pages
        self.has_prev = self.page > 1
        self.next_page = self.page + 1 if self.has_next else None
        self.prev_page = self.page - 1 if self.has_prev else None
        return self

    @classmethod
    def from_paged(cls, items: list[T], total: int, page: int, per_page: int) -> "PaginatedList[T]":
        return cls(items=items, total=total, page=page, per_page=per_page)
