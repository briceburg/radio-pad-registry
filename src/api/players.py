from types import MappingProxyType
from fastapi import APIRouter, HTTPException, Path, Query

from lib.helpers import build_paginated_response
from models.player import Player, PlayerList
from models.pagination import PaginatedResponse

router = APIRouter()


@router.get("/players/{account}/{id}", response_model=Player)
async def get(
    account: str = Path(..., description="Player Account", example="briceburg"),
    id: str = Path(..., description="Player ID", example="living-room")
):
    """Get a player by account and ID - maps to GET /players/{account}/{id}"""
    players = PLAYERS.get(account, {})
    player = players.get(id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player_data = dict(player)
    player_data["id"] = id
    player_data["account"] = account

    if not player_data.get("stationsUrl"):
        player_data["stationsUrl"] = f"https://registry.radiopad.dev/v1/stations/briceburg"
    if not player_data.get("switchboardUrl"):
        player_data["switchboardUrl"] = f"wss://switchboard.radiopad.dev/{account}/{id}"

    return Player(**player_data)


@router.get("/players/{account}", response_model=PaginatedResponse[PlayerList])
async def search(
    account: str = Path(..., description="Player Account", example="briceburg"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page", alias="perPage")
):
    """List all players for an account - maps to GET /players/{account} with pagination"""
    players = PLAYERS.get(account, {})
    players_list = [{"id": id, "name": p.get("name")} for id, p in players.items()]

    return build_paginated_response(players_list, PlayerList, page, per_page)


def _load_players():
    # Example: namespaced players
    players = {
        "briceburg": {
            "living-room": {"name": "Living Room"},
            "kitchen": {"name": "Kitchen"},
        },
        "otheruser": {"office": {"name": "Office"}},
    }
    return MappingProxyType(players)


PLAYERS = _load_players()
