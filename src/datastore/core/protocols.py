from __future__ import annotations

from typing import Any, Protocol

from lib.types import ValueWithVersion


class ObjectStore(Protocol):
    def get(self, object_id: str, *path: str) -> ValueWithVersion[dict[str, Any]]: ...

    def list(self, *path: str, page: int = 1, per_page: int = 10) -> tuple[list[dict[str, Any]], int]: ...

    def save(self, object_id: str, data: dict[str, Any], *path: str, if_match: str | None = None) -> None: ...

    def delete(self, object_id: str, *path: str) -> bool: ...
