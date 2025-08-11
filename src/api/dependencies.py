from typing import cast

from fastapi import HTTPException, Query, Request

from datastore import DataStore

MAX_PER_PAGE = 100


def get_store(request: Request) -> DataStore:
    ds = getattr(request.app.state, "store", None)
    if ds is None or not isinstance(ds, DataStore):
        raise HTTPException(status_code=500, detail="Datastore not initialized")
    return cast(DataStore, ds)


def pagination(
    page: int = Query(1, ge=1, description="Page number (>=1)"),
    per_page: int = Query(10, ge=1, le=MAX_PER_PAGE, description="Items per page (1-100)"),
) -> dict[str, int]:
    return {"page": page, "per_page": per_page}


__all__ = ["MAX_PER_PAGE", "get_store", "pagination"]
