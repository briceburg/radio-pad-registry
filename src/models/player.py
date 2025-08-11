from typing import Any

from pydantic import BaseModel, Field, HttpUrl, model_validator

from lib.constants import SLUG_PATTERN


class PlayerBase(BaseModel):
    """Base model for players, containing common fields."""

    name: str = Field(..., json_schema_extra={"example": "Living Room"})
    stations_url: HttpUrl | None = Field(
        None,
        json_schema_extra={"example": "https://registry.radiopad.dev/v1/presets/briceburg"},
    )
    switchboard_url: str | None = Field(
        None,
        json_schema_extra={"example": "wss://switchboard.radiopad.dev/briceburg/custom-player"},
    )


class PlayerCreate(PlayerBase):
    """
    Request body model for creating/updating a player via the PUT endpoint.
    The Player validator provides default station and switchboard URLs.
    """


class Player(PlayerBase):
    """The full player model as stored and returned by the API."""

    id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "living-room", "pattern": SLUG_PATTERN},
    )
    account_id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "briceburg", "pattern": SLUG_PATTERN},
    )

    @model_validator(mode="before")
    @classmethod
    def set_default_urls(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("stations_url"):
                data["stations_url"] = "https://registry.radiopad.dev/v1/presets/briceburg"
            if not data.get("switchboard_url"):
                data["switchboard_url"] = f"wss://switchboard.radiopad.dev/{data.get('account_id')}/{data.get('id')}"
        return data
