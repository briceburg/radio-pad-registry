from datastore.backends.json_file_store import JSONFileStore
from datastore.model_store import ModelStore
from models.player import Player


class Players(ModelStore[Player]):
    """A data store for managing an account's players (accounts/<account_id>/players/<id>.json)."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(
            file_store,
            model=Player,
            path_template="accounts/{account_id}/players/{id}",
        )
