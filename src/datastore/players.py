from datastore.backends.json_file_store import JSONFileStore
from models.player import Player

from .base import BaseAccountScopedRepo


class Players(BaseAccountScopedRepo[Player]):
    """A data store for managing an account's players."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, "players", Player)
