from datastore.backends.json_file_store import JSONFileStore
from models.station_preset import GlobalStationPreset, AccountStationPreset
from .base import BaseFlatRepo, BaseAccountScopedRepo

class GlobalPresets(BaseFlatRepo[GlobalStationPreset]):
    """Repository for global station presets (presets/<id>.json)."""
    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, "presets", GlobalStationPreset)

class AccountPresets(BaseAccountScopedRepo[AccountStationPreset]):
    """Repository for account-scoped station presets (accounts/<account_id>/presets/<id>.json)."""
    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, "presets", AccountStationPreset)
