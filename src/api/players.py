# This file will be imported by the RestyResolver
# Functions will be mapped to API endpoints automatically:
# GET /players/{player_id} -> get(player_id)
# GET /players -> search()

import connexion
from starlette.responses import JSONResponse, Response
from api import response

# We'll store a reference to the app globally to access PLAYERS data
_app_instance = None


def set_app_instance(app):
    """Set the app instance to access player data"""
    global _app_instance
    _app_instance = app


async def get(player_id):
    """Get a player by ID - maps to GET /players/{player_id}"""
    player = _app_instance.PLAYERS.get(player_id)
    if player is None:
        return response({"error": "Player not found"}, status=404)

    # Make a shallow copy for fallback fields
    player = dict(player)

    if not player.get("stationsUrl"):
        player["stationsUrl"] = (
            f"https://registry.radiopad.dev/players/{player_id}/stations.json"
        )

    if not player.get("switchboardUrl"):
        player["switchboardUrl"] = f"wss://{player_id}.player-switchboard.radiopad.dev"

    return response(player, root="player")


async def search():
    """List all players - maps to GET /players"""
    # TODO: Implement pagination
    return response(_app_instance.PLAYERS_SUMMARY, root="players")