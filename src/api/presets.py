from fastapi import APIRouter, Depends, HTTPException

from models.pagination import PaginatedList
from models.station_preset import (
    AccountStationPreset,
    AccountStationPresetCreate,
    GlobalStationPreset,
    GlobalStationPresetCreate,
)
from datastore import DataStore
from .deps import get_store, pagination

router = APIRouter()


@router.put(
    "/accounts/{account_id}/presets/{preset_id}",
    response_model=AccountStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def register_account_preset(
    account_id: str,
    preset_id: str,
    preset_data: AccountStationPresetCreate,
    ds: DataStore = Depends(get_store),
):
    """Create or update an account station preset."""
    preset = AccountStationPreset(id=preset_id, account_id=account_id, **preset_data.model_dump())
    return ds.account_presets.save(preset)


@router.put(
    "/presets/{preset_id}",
    response_model=GlobalStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def register_global_preset(
    preset_id: str,
    preset_data: GlobalStationPresetCreate,
    ds: DataStore = Depends(get_store),
):
    """Create or update a global station preset."""
    preset = GlobalStationPreset(id=preset_id, **preset_data.model_dump())
    return ds.global_presets.save(preset)


@router.get(
    "/accounts/{account_id}/presets/{preset_id}",
    response_model=AccountStationPreset,
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def get_account_preset(
    account_id: str,
    preset_id: str,
    ds: DataStore = Depends(get_store),
):
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
    preset_id: str,
    ds: DataStore = Depends(get_store),
):
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
    account_id: str,
    params: dict = Depends(pagination),
    ds: DataStore = Depends(get_store),
):
    """
    List account station presets.
    """
    return ds.account_presets.list(account_id=account_id, **params)


@router.get(
    "/presets",
    response_model=PaginatedList[GlobalStationPreset],
    response_model_exclude_none=True,
    tags=["station presets"],
)
async def list_global_presets(
    params: dict = Depends(pagination),
    ds: DataStore = Depends(get_store),
):
    """List all available global station presets."""
    return ds.global_presets.list(**params)