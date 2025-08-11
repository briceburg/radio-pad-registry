from pydantic import BaseModel, Field, HttpUrl

from lib.constants import SLUG_PATTERN


class Station(BaseModel):
    """A single station within a preset."""

    name: str = Field(..., json_schema_extra={"example": "WWOZ"})
    url: HttpUrl = Field(..., json_schema_extra={"example": "https://www.wwoz.org/listen/hi"})
    color: str | None = Field(
        default=None,
        pattern=r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$",
        json_schema_extra={"example": "#FF5733"},
    )


class StationPresetBase(BaseModel):
    """Base model for station presets, containing common fields."""

    name: str = Field(..., json_schema_extra={"example": "My Favorite Stations"})
    category: str | None = Field(None, json_schema_extra={"example": "News"})
    description: str | None = Field(
        None,
        json_schema_extra={"example": "A collection of my favorite news stations."},
    )
    stations: list[Station]


class GlobalStationPresetCreate(StationPresetBase):
    """Request body model for creating a global station preset."""

    pass


class AccountStationPresetCreate(StationPresetBase):
    """Request body model for creating an account station preset."""

    pass


class GlobalStationPreset(StationPresetBase):
    """A global station preset."""

    id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "briceburg"},
    )


class AccountStationPreset(StationPresetBase):
    """An account-specific station preset."""

    id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "briceburg-my-favorites"},
    )
    account_id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "briceburg"},
    )
