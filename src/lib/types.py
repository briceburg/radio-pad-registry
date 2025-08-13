from __future__ import annotations

from typing import Any, Mapping, NewType, TypeVar

T = TypeVar("T")

# Raw (items, total) tuple returned by low-level listing functions before wrapping in PaginatedList.
type PagedResult[T] = tuple[list[T], int]

# Version token (e.g., ETag, VersionId)
type Version = str

# Standardized (value, version) tuple used by object stores
# Example: ValueWithVersion[dict[str, Any]]
type ValueWithVersion[T] = tuple[T | None, Version | None]

# Datastore-related common types
# Mapping of required path parameters extracted from path templates
type PathParams = Mapping[str, str]
# Opaque raw JSON document stored at rest
type RawDoc = dict[str, Any]
# Directory components computed from path templates
type DirComponents = tuple[str, ...]

# Optional stronger semantic aliases
ObjectId = NewType("ObjectId", str)
PathTemplate = NewType("PathTemplate", str)

__all__ = [
    "PagedResult",
    "Version",
    "ValueWithVersion",
    "PathParams",
    "RawDoc",
    "DirComponents",
    "ObjectId",
    "PathTemplate",
]
