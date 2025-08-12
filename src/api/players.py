from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DS, AccountId, PlayerId, PageParams
from models import Account, PaginatedList, Player, PlayerCreate

router = APIRouter(prefix="/accounts/{account_id}/players", tags=["players"])


@router.put("/{player_id}", response_model=Player)
async def register_player(
    account_id: AccountId,
    player_id: PlayerId,
    ds: DS,
    player_data: PlayerCreate | None = None,
) -> Player:
    """Register or update a player. Creates the account if it doesn't exist."""
    if ds.accounts.get(account_id) is None:
        new_account = Account(id=account_id, name=account_id)
        ds.accounts.save(new_account)
    partial = player_data.model_dump(exclude_unset=True) if player_data else {}
    player = ds.players.merge_upsert(player_id, partial, path_params={"account_id": account_id})
    return player


@router.get("/{player_id}", response_model=Player)
async def get_player(
    account_id: AccountId,
    player_id: PlayerId,
    ds: DS,
) -> Player:
    """Get a player by account and ID"""
    player = ds.players.get(player_id, path_params={"account_id": account_id})
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("", response_model=PaginatedList[Player], include_in_schema=False)
@router.get("/", response_model=PaginatedList[Player])
async def list_players(
    account_id: AccountId,
    ds: DS,
    paging: PageParams,
) -> PaginatedList[Player]:
    """List all players for an account"""
    return ds.players.list(path_params={"account_id": account_id}, page=paging.page, per_page=paging.per_page)
