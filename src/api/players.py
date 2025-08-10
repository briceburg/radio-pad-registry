from fastapi import APIRouter, Depends, HTTPException

from models.account import Account
from models.pagination import PaginatedList
from models.player import Player, PlayerCreate
from datastore import DataStore
from .deps import get_store

router = APIRouter()


@router.put("/accounts/{account_id}/players/{player_id}", response_model=Player)
async def register_player(account_id: str, player_id: str, player_data: PlayerCreate, ds: DataStore = Depends(get_store)):
    """Register or update a player. Creates the account if it doesn't exist."""
    # Ensure the account exists
    if ds.accounts.get(account_id) is None:
        new_account = Account(id=account_id, name=account_id)
        ds.accounts.save(new_account)

    # Check if player exists to update it, otherwise create a new one
    existing_player = ds.players.get(account_id, player_id)
    if existing_player:
        # Update existing player
        update_data = player_data.model_dump(exclude_unset=True)
        updated_player = existing_player.model_copy(update=update_data)
        return ds.players.save(updated_player)
    else:
        # Create new player
        player = Player(id=player_id, account_id=account_id, **player_data.model_dump())
        return ds.players.save(player)


@router.get("/accounts/{account_id}/players/{player_id}", response_model=Player)
async def get_player(account_id: str, player_id: str, ds: DataStore = Depends(get_store)):
    """Get a player by account and ID"""
    player = ds.players.get(account_id, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/accounts/{account_id}/players", response_model=PaginatedList[Player])
async def list_players(account_id: str, page: int = 1, per_page: int = 10, ds: DataStore = Depends(get_store)):
    """List all players for an account"""
    return ds.players.list(account_id, page=page, per_page=per_page)
