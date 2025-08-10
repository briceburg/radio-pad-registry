from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Station(BaseModel):
    """A single station within a preset."""

    name: str = Field(..., json_schema_extra={"example": "WWOZ"})
    url: HttpUrl = Field(
        ..., json_schema_extra={"example": "https://www.wwoz.org/listen/hi"}
    )
    color: Optional[str] = Field(
        default=None,
        pattern=r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$",
        json_schema_extra={"example": "#FF5733"},
    )


class StationPresetBase(BaseModel):
    """Base model for station presets, containing common fields."""

    name: str = Field(..., json_schema_extra={"example": "My Favorite Stations"})
    category: Optional[str] = Field(None, json_schema_extra={"example": "News"})
    description: Optional[str] = Field(
        None,
        json_schema_extra={"example": "A collection of my favorite news stations."},
    )
    stations: List[Station]


class GlobalStationPresetCreate(StationPresetBase):
    """Request body model for creating a global station preset."""

    pass


class AccountStationPresetCreate(StationPresetBase):
    """Request body model for creating an account station preset."""

    pass


class GlobalStationPreset(StationPresetBase):
    """A global station preset."""

    id: str = Field(..., json_schema_extra={"example": "briceburg"})


class AccountStationPreset(StationPresetBase):
    """An account-specific station preset."""

    id: str = Field(..., json_schema_extra={"example": "briceburg-my-favorites"})
    account_id: str = Field(..., json_schema_extra={"example": "briceburg"})