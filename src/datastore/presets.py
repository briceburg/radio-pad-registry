from datastore.backends.json_file_store import JSONFileStore
from datastore.model_store import ModelStore
from models.station_preset import AccountStationPreset, GlobalStationPreset


class GlobalPresets(ModelStore[GlobalStationPreset]):
    """Repository for global station presets (presets/<id>.json)."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, model=GlobalStationPreset, path_template="presets/{id}")


class AccountPresets(ModelStore[AccountStationPreset]):
    """Repository for account-scoped station presets (accounts/<account_id>/presets/<id>.json)."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(
            file_store,
            model=AccountStationPreset,
            path_template="accounts/{account_id}/presets/{id}",
        )
