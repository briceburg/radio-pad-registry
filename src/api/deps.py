from fastapi import Depends, HTTPException, Request
from datastore import DataStore


def get_store(request: Request) -> DataStore:
    ds = getattr(request.app.state, "store", None)
    if ds is None:
        raise HTTPException(status_code=500, detail="Datastore not initialized")
    return ds


def pagination(page: int = 1, per_page: int = 10):
    return {"page": page, "per_page": per_page}
