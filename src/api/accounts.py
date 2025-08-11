from fastapi import APIRouter, Depends, Path

from api.dependencies import get_store, pagination
from datastore import DataStore
from lib.constants import SLUG_PATTERN
from models.account import Account, AccountCreate
from models.pagination import PaginatedList

router = APIRouter()


@router.put("/accounts/{id}", response_model=Account)
async def register_account(
    id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    account_data: AccountCreate | None = None,
    ds: DataStore = Depends(get_store),
) -> Account:
    """Register or update an account (partial PUT semantics)."""
    partial = account_data.model_dump(exclude_unset=True) if account_data else {}
    account = ds.accounts.merge_upsert(id, partial)
    return account


@router.get("/accounts", response_model=PaginatedList[Account])
async def list_accounts(
    params: dict[str, int] = Depends(pagination), ds: DataStore = Depends(get_store)
) -> PaginatedList[Account]:
    """List all accounts"""
    return ds.accounts.list(**params)
