from fastapi import APIRouter, Depends

from models.account import Account, AccountCreate
from models.pagination import PaginatedList
from datastore import DataStore
from .deps import get_store

router = APIRouter()


@router.put("/accounts/{id}", response_model=Account)
async def register_account(id: str, account_data: AccountCreate, ds: DataStore = Depends(get_store)):
    """Register an account"""
    account = Account(id=id, **account_data.model_dump())
    return ds.accounts.save(account)


@router.get("/accounts", response_model=PaginatedList[Account])
async def list_accounts(page: int = 1, per_page: int = 10, ds: DataStore = Depends(get_store)):
    """List all accounts"""
    return ds.accounts.list(page=page, per_page=per_page)