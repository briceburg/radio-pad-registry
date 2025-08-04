import json
from datetime import datetime
from types import MappingProxyType
from fastapi import APIRouter, HTTPException, Path, Query

from lib.constants import BASE_DIR
from lib.helpers import build_paginated_response, logger
from lib.schema import validate_schema
from models.station import StationList
from models.station_preset import StationPresetList
from models.pagination import PaginatedResponse

router = APIRouter()


@router.get("/station-presets/{id}", response_model=StationList)
async def get(id: str = Path(..., description="Station Preset ID", example="briceburg")):
    """Get a Station Preset by ID - maps to GET /station-presets/{id}"""
    
    preset = STATION_PRESETS.get(id)
    if preset is None:
        raise HTTPException(status_code=404, detail="Preset not found")

    # Return the preset data as StationList
    return StationList(root=preset)


@router.get("/station-presets", response_model=PaginatedResponse[StationPresetList])
async def search(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page", alias="perPage")
):
    """List all station presets - maps to GET /station-presets with pagination"""
    
    return build_paginated_response(
        list(STATION_PRESETS_LIST), StationPresetList, page, per_page
    )


def _load_station_presets():
    stations_dir = BASE_DIR / "station-presets"
    station_presets = {}

    for station_file in stations_dir.glob("*.json"):
        with open(station_file, "r") as f:
            stations = json.load(f)
            is_valid, err = validate_schema("StationList", stations)
            if is_valid:
                station_presets[station_file.stem] = stations
            else:
                logger.error(f"Invalid station-presets file: {station_file}: {err}")

    return MappingProxyType(station_presets), tuple(
        {"id": k, "lastUpdated": datetime.now().isoformat(timespec="seconds")}
        for k in station_presets.keys()
    )


STATION_PRESETS, STATION_PRESETS_LIST = _load_station_presets()
