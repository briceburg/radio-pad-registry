from fastapi import APIRouter, Depends, HTTPException, Path

from api.dependencies import get_store, pagination
from datastore import DataStore
from lib.constants import SLUG_PATTERN
from models.account import Account
from models.pagination import PaginatedList
from models.player import Player, PlayerCreate

router = APIRouter()


@router.put("/accounts/{account_id}/players/{player_id}", response_model=Player)
async def register_player(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    player_id: str = Path(..., pattern=SLUG_PATTERN, description="Player ID (slug)"),
    player_data: PlayerCreate | None = None,
    ds: DataStore = Depends(get_store),
) -> Player:
    """Register or update a player. Creates the account if it doesn't exist."""
    if ds.accounts.get(account_id) is None:
        new_account = Account(id=account_id, name=account_id)
        ds.accounts.save(new_account)
    partial = player_data.model_dump(exclude_unset=True) if player_data else {}
    player = ds.players.merge_upsert(account_id, player_id, partial)
    return player


@router.get("/accounts/{account_id}/players/{player_id}", response_model=Player)
async def get_player(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    player_id: str = Path(..., pattern=SLUG_PATTERN, description="Player ID (slug)"),
    ds: DataStore = Depends(get_store),
) -> Player:
    """Get a player by account and ID"""
    player = ds.players.get(account_id, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/accounts/{account_id}/players", response_model=PaginatedList[Player])
async def list_players(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    params: dict[str, int] = Depends(pagination),
    ds: DataStore = Depends(get_store),
) -> PaginatedList[Player]:
    """List all players for an account"""
    return ds.players.list(account_id, **params)
