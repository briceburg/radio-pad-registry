from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DS, AccountId, PresetId, PageParams
from models import (
    AccountStationPreset,
    AccountStationPresetCreate,
    GlobalStationPreset,
    GlobalStationPresetCreate,
    PaginatedList,
)

# Split routers: account-scoped and global
account_presets = APIRouter(prefix="/accounts/{account_id}/presets", tags=["station presets"])
global_presets = APIRouter(prefix="/presets", tags=["station presets"])


# --- Account-scoped Presets ---
@account_presets.put("/{preset_id}", response_model=AccountStationPreset, response_model_exclude_none=True)
async def register_account_preset(
    account_id: AccountId,
    preset_id: PresetId,
    ds: DS,
    preset_data: AccountStationPresetCreate | None = None,
) -> AccountStationPreset:
    """Create or update an account station preset (partial PUT semantics)."""
    partial = preset_data.model_dump(exclude_unset=True) if preset_data else {}
    preset = ds.account_presets.merge_upsert(preset_id, partial, path_params={"account_id": account_id})
    return preset


@account_presets.get("/{preset_id}", response_model=AccountStationPreset, response_model_exclude_none=True)
async def get_account_preset(
    account_id: AccountId,
    preset_id: PresetId,
    ds: DS,
) -> AccountStationPreset:
    """Get a single account station preset by its ID."""
    preset = ds.account_presets.get(preset_id, path_params={"account_id": account_id})
    if preset is None:
        raise HTTPException(status_code=404, detail="Station preset not found")
    return preset


@account_presets.get("", response_model=PaginatedList[AccountStationPreset], response_model_exclude_none=True, include_in_schema=False)
@account_presets.get("/", response_model=PaginatedList[AccountStationPreset], response_model_exclude_none=True)
async def list_account_presets(
    account_id: AccountId,
    ds: DS,
    paging: PageParams,
) -> PaginatedList[AccountStationPreset]:
    """List account station presets."""
    return ds.account_presets.list(path_params={"account_id": account_id}, page=paging.page, per_page=paging.per_page)


# --- Global Presets ---
@global_presets.put("/{preset_id}", response_model=GlobalStationPreset, response_model_exclude_none=True)
async def register_global_preset(
    preset_id: PresetId,
    ds: DS,
    preset_data: GlobalStationPresetCreate | None = None,
) -> GlobalStationPreset:
    """Create or update a global station preset (partial PUT semantics)."""
    partial = preset_data.model_dump(exclude_unset=True) if preset_data else {}
    preset = ds.global_presets.merge_upsert(preset_id, partial)
    return preset


@global_presets.get("/{preset_id}", response_model=GlobalStationPreset, response_model_exclude_none=True)
async def get_global_preset(
    preset_id: PresetId,
    ds: DS,
) -> GlobalStationPreset:
    """Get a single global station preset by its ID."""
    preset = ds.global_presets.get(preset_id)
    if preset is None:
        raise HTTPException(status_code=404, detail="Station preset not found")
    return preset


@global_presets.get("", response_model=PaginatedList[GlobalStationPreset], response_model_exclude_none=True, include_in_schema=False)
@global_presets.get("/", response_model=PaginatedList[GlobalStationPreset], response_model_exclude_none=True)
async def list_global_presets(
    ds: DS,
    paging: PageParams,
) -> PaginatedList[GlobalStationPreset]:
    """List all available global station presets."""
    return ds.global_presets.list(page=paging.page, per_page=paging.per_page)
