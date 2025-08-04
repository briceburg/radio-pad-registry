from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, AnyUrl


class Player(BaseModel):
    """Player model."""
    id: str = Field(..., description="Unique identifier for the player", example="living-room")
    name: str = Field(..., description="Display name of the player", example="Living Room")
    account: Optional[str] = Field(None, description="Account the player belongs to", example="briceburg")
    stationsUrl: HttpUrl = Field(..., description="URL to the player's station list", example="https://registry.radiopad.dev/v1/stations/briceburg")
    switchboardUrl: AnyUrl = Field(..., description="WebSocket URL for the player's switchboard", example="wss://switchboard.radiopad.dev/briceburg/living-room")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "living-room",
                "name": "Living Room",
                "account": "briceburg",
                "stationsUrl": "https://registry.radiopad.dev/v1/stations/briceburg",
                "switchboardUrl": "wss://switchboard.radiopad.dev/briceburg/living-room"
            }
        }
    }


class PlayerList(BaseModel):
    """Player list item for pagination."""
    id: str = Field(..., description="Unique identifier for the player", example="living-room")
    name: str = Field(..., description="Display name of the player", example="Living Room")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "living-room",
                "name": "Living Room"
            }
        }
    }