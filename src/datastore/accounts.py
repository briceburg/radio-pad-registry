from datastore.backends.json_file_store import JSONFileStore
from models.account import Account
from models.pagination import PaginatedList
from .base import BaseFlatRepo


class Accounts(BaseFlatRepo[Account]):
    """A data store for managing accounts."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, "accounts", Account)
