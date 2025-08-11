from fastapi import APIRouter, Depends, HTTPException, Path

from api.dependencies import get_store, pagination
from datastore import DataStore
from lib.constants import SLUG_PATTERN
from models.pagination import PaginatedList
from models.station_preset import (
    AccountStationPreset,
    AccountStationPresetCreate,
    GlobalStationPreset,
    GlobalStationPresetCreate,
)

router = APIRouter()


@router.put(
    "/accounts/{account_id}/presets/{preset_id}",
    response_model=AccountStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def register_account_preset(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    preset_id: str = Path(..., pattern=SLUG_PATTERN, description="Preset ID (slug)"),
    preset_data: AccountStationPresetCreate | None = None,
    ds: DataStore = Depends(get_store),
) -> AccountStationPreset:
    """Create or update an account station preset (partial PUT semantics)."""
    partial = preset_data.model_dump(exclude_unset=True) if preset_data else {}
    preset = ds.account_presets.merge_upsert(account_id, preset_id, partial)
    return preset


@router.put(
    "/presets/{preset_id}",
    response_model=GlobalStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def register_global_preset(
    preset_id: str = Path(..., pattern=SLUG_PATTERN, description="Preset ID (slug)"),
    preset_data: GlobalStationPresetCreate | None = None,
    ds: DataStore = Depends(get_store),
) -> GlobalStationPreset:
    """Create or update a global station preset (partial PUT semantics)."""
    partial = preset_data.model_dump(exclude_unset=True) if preset_data else {}
    preset = ds.global_presets.merge_upsert(preset_id, partial)
    return preset


@router.get(
    "/accounts/{account_id}/presets/{preset_id}",
    response_model=AccountStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def get_account_preset(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    preset_id: str = Path(..., pattern=SLUG_PATTERN, description="Preset ID (slug)"),
    ds: DataStore = Depends(get_store),
) -> AccountStationPreset:
    """Get a single account station preset by its ID."""
    preset = ds.account_presets.get(account_id, preset_id)
    if preset is None:
        raise HTTPException(status_code=404, detail="Station preset not found")
    return preset


@router.get(
    "/presets/{preset_id}",
    response_model=GlobalStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def get_global_preset(
    preset_id: str = Path(..., pattern=SLUG_PATTERN, description="Preset ID (slug)"),
    ds: DataStore = Depends(get_store),
) -> GlobalStationPreset:
    """Get a single global station preset by its ID."""
    preset = ds.global_presets.get(preset_id)
    if preset is None:
        raise HTTPException(status_code=404, detail="Station preset not found")
    return preset


@router.get(
    "/accounts/{account_id}/presets",
    response_model=PaginatedList[AccountStationPreset],
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def list_account_presets(
    account_id: str = Path(..., pattern=SLUG_PATTERN, description="Account ID (slug)"),
    params: dict[str, int] = Depends(pagination),
    ds: DataStore = Depends(get_store),
) -> PaginatedList[AccountStationPreset]:
    """List account station presets."""
    return ds.account_presets.list(account_id=account_id, **params)


@router.get(
    "/presets",
    response_model=PaginatedList[GlobalStationPreset],
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def list_global_presets(
    params: dict[str, int] = Depends(pagination),
    ds: DataStore = Depends(get_store),
) -> PaginatedList[GlobalStationPreset]:
    """List all available global station presets."""
    return ds.global_presets.list(**params)
