from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field, RootModel


class Station(BaseModel):
    """Station model."""
    name: str = Field(..., description="Name of the station", example="WWOZ")
    url: HttpUrl = Field(..., description="Streaming URL of the station", example="https://www.wwoz.org/listen/hi")
    color: Optional[str] = Field(
        default="#000077",
        description="Optional color associated with the station, in hex format",
        pattern=r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$",
        example="#000077"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "WWOZ",
                "url": "https://www.wwoz.org/listen/hi",
                "color": "#000077"
            }
        }
    }


class StationList(RootModel[List[Station]]):
    """List of stations."""
    root: List[Station]

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "name": "WWOZ",
                    "url": "https://www.wwoz.org/listen/hi",
                    "color": "#000077"
                }
            ]
        }
    }