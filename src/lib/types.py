from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")

# Raw (items, total) tuple returned by low-level listing functions before wrapping in PaginatedList.
type PagedResult[T] = tuple[list[T], int]

__all__ = ["PagedResult"]
