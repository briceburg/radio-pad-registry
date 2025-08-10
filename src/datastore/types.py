from __future__ import annotations
from typing import TypeVar, TypeAlias

T = TypeVar("T")

# PagedResult[T] represents the raw (items, total) pattern returned by low-level
# store list operations before wrapping into higher-level PaginatedList models.
PagedResult: TypeAlias = tuple[list[T], int]
