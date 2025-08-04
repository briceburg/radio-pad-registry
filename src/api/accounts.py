from types import MappingProxyType
from fastapi import APIRouter, Query

from lib.helpers import build_paginated_response
from models.account import AccountList
from models.pagination import PaginatedResponse

router = APIRouter()


@router.get("/accounts", response_model=PaginatedResponse[AccountList])
async def search(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page", alias="perPage")
):
    """List all accounts - maps to GET /accounts"""
    
    account_list = [
        {"id": id, "name": account.get("name", id.replace("_", " ").title())}
        for id, account in ACCOUNTS.items()
    ]

    return build_paginated_response(account_list, AccountList, page, per_page)


def _load_accounts():
    accounts = {"briceburg": {}}
    return MappingProxyType(accounts)


ACCOUNTS = _load_accounts()
