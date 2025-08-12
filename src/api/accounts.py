from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DS, AccountId, PageParams
from models import Account, AccountCreate, PaginatedList

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.put("/{account_id}", response_model=Account)
async def register_account(
    account_id: AccountId,
    ds: DS,
    account_data: AccountCreate | None = None,
) -> Account:
    """Register or update an account."""
    partial = account_data.model_dump(exclude_unset=True) if account_data else {}
    account = ds.accounts.merge_upsert(account_id, partial)
    return account


@router.get("/{account_id}", response_model=Account)
async def get_account(
    account_id: AccountId,
    ds: DS,
) -> Account:
    """Get an account by its ID."""
    account = ds.accounts.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("", response_model=PaginatedList[Account], include_in_schema=False)
@router.get("/", response_model=PaginatedList[Account])
async def list_accounts(
    ds: DS,
    paging: PageParams,
) -> PaginatedList[Account]:
    """List all accounts."""
    return ds.accounts.list(page=paging.page, per_page=paging.per_page)
