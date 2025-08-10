from __future__ import annotations
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from datastore.backends.json_file_store import JSONFileStore
from models.pagination import PaginatedList

# TypeVar usage: TModel = TypeVar("TModel", bound=BaseModel) defines a generic type parameter 
# constrained to subclasses of Pydantic BaseModel. 
# It lets BaseFlatRepo[TModel] and BaseAccountScopedRepo[TModel] be type‑safe: 
# methods return the specific model class you pass (Account, Player, etc.) instead of plain BaseModel.
TModel = TypeVar("TModel", bound=BaseModel)


class BaseFlatRepo(Generic[TModel]):
    """Repository for models stored under a single root directory using filename-derived IDs."""
    def __init__(self, file_store: JSONFileStore, root_dir: str, model: Type[TModel]):
        self._file_store = file_store
        self._root_dir = root_dir
        self._model = model

    def get(self, object_id: str) -> TModel | None:
        data = self._file_store.get(object_id, self._root_dir)
        if data is None:
            return None
        # Ensure id present for validation
        return self._model.model_validate({"id": object_id, **data})

    def list(self, page: int = 1, per_page: int = 10) -> PaginatedList[TModel]:
        items, total = self._file_store.list(self._root_dir, page=page, per_page=per_page)
        models = [self._model.model_validate(item) for item in items]
        return PaginatedList(items=models, total=total, page=page, per_page=per_page)

    def save(self, model_obj: TModel) -> TModel:
        data = model_obj.model_dump(mode="json")
        data.pop("id", None)
        self._file_store.save(model_obj.id, data, self._root_dir)
        return model_obj


class BaseAccountScopedRepo(Generic[TModel]):
    """Repository for account-scoped models stored under accounts/<account_id>/<sub_dir>/<id>.json."""
    def __init__(self, file_store: JSONFileStore, sub_dir: str, model: Type[TModel]):
        self._file_store = file_store
        self._sub_dir = sub_dir
        self._model = model

    def get(self, account_id: str, object_id: str) -> TModel | None:
        data = self._file_store.get(object_id, "accounts", account_id, self._sub_dir)
        if data is None:
            return None
        data.pop("id", None)
        data.pop("account_id", None)
        return self._model.model_validate({"id": object_id, "account_id": account_id, **data})

    def list(self, account_id: str, page: int = 1, per_page: int = 10) -> PaginatedList[TModel]:
        items, total = self._file_store.list("accounts", account_id, self._sub_dir, page=page, per_page=per_page)
        models: list[TModel] = []
        for item in items:
            file_id = item.get("id")
            item.pop("id", None)
            item.pop("account_id", None)
            models.append(self._model.model_validate({"id": file_id, "account_id": account_id, **item}))
        return PaginatedList(items=models, total=total, page=page, per_page=per_page)

    def save(self, model_obj: TModel) -> TModel:
        data = model_obj.model_dump(mode="json")
        for k in ("id", "account_id"):
            data.pop(k, None)
        self._file_store.save(model_obj.id, data, "accounts", model_obj.account_id, self._sub_dir)
        return model_obj
