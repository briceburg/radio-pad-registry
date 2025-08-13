from typing import cast, Annotated

from fastapi import HTTPException, Query, Request, Depends, Path

from datastore import DataStore
from lib import SLUG_PATTERN
from models.pagination import PaginationParams

MAX_PER_PAGE = 100


def get_store(request: Request) -> DataStore:
    ds = getattr(request.app.state, "store", None)
    if ds is None or not isinstance(ds, DataStore):
        raise HTTPException(status_code=500, detail="Datastore not initialized")
    return cast(DataStore, ds)


# Typed alias for injecting the DataStore (easy to override in tests via get_store)
DS = Annotated[DataStore, Depends(get_store)]


def pagination(
    page: int = Query(1, ge=1, description="Page number (>=1)"),
    per_page: int = Query(10, ge=1, le=MAX_PER_PAGE, description="Items per page (1-100)"),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)


# Annotated alias for pagination dependency
PageParams = Annotated[PaginationParams, Depends(pagination)]


# Common path param aliases
AccountId = Annotated[str, Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)")]
PlayerId = Annotated[str, Path(..., pattern=SLUG_PATTERN, description="Player ID (slug)")]
PresetId = Annotated[str, Path(..., pattern=SLUG_PATTERN, description="Preset ID (slug)")]


__all__ = [
    "MAX_PER_PAGE",
    "get_store",
    "pagination",
    "DS",
    "PageParams",
    "AccountId",
    "PlayerId",
    "PresetId",
]
