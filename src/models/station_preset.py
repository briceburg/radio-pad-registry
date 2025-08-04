from datetime import datetime
from pydantic import BaseModel, Field


class StationPreset(BaseModel):
    """Station preset model."""
    id: str = Field(..., description="Unique identifier for the station preset", example="briceburg")
    lastUpdated: datetime = Field(..., description="Last updated timestamp", example="2025-10-01T12:00:00Z")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "briceburg",
                "lastUpdated": "2025-10-01T12:00:00Z"
            }
        }
    }


class StationPresetList(BaseModel):
    """Station preset list item for pagination."""
    id: str = Field(..., description="Unique identifier for the station preset", example="briceburg")
    lastUpdated: datetime = Field(..., description="Last updated timestamp", example="2025-10-01T12:00:00Z")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "briceburg",
                "lastUpdated": "2025-10-01T12:00:00Z"
            }
        }
    }