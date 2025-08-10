from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl, model_validator


class PlayerBase(BaseModel):
    """Base model for players, containing common fields."""

    name: str = Field(..., json_schema_extra={"example": "Living Room"})
    stations_url: Optional[HttpUrl] = Field(
        None,
        json_schema_extra={
            "example": "https://registry.radiopad.dev/v1/stations/custom-preset"
        },
    )
    switchboard_url: Optional[str] = Field(
        None,
        json_schema_extra={
            "example": "wss://switchboard.radiopad.dev/briceburg/custom-player"
        },
    )


class PlayerCreate(PlayerBase):
    """
    Request body model for creating/updating a player via the PUT endpoint.
    The Player validator provides default station and switchboard URLs.
    """


class Player(PlayerBase):
    """The full player model as stored and returned by the API."""

    id: str = Field(..., json_schema_extra={"example": "living-room"})
    account_id: str = Field(..., json_schema_extra={"example": "briceburg"})

    @model_validator(mode="before")
    @classmethod
    def set_default_urls(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("stations_url"):
                data["stations_url"] = (
                    f"https://registry.radiopad.dev/v1/presets/briceburg"
                )
            if not data.get("switchboard_url"):
                data["switchboard_url"] = (
                    f"wss://switchboard.radiopad.dev/{data.get('account_id')}/{data.get('id')}"
                )
        return data
