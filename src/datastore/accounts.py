from datastore.backends.json_file_store import JSONFileStore
from datastore.model_store import ModelStore
from models.account import Account


class Accounts(ModelStore[Account]):
    """A data store for managing accounts (accounts/<id>.json)."""

    def __init__(self, file_store: JSONFileStore):
        super().__init__(file_store, model=Account, path_template="accounts/{id}")
