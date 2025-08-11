from __future__ import annotations

from typing import Any, Protocol, Self, TypedDict

from datastore.backends.json_file_store import JSONFileStore
from models.pagination import PaginatedList


class PartialDict(TypedDict, total=False):
    pass


class PydanticModel(Protocol):
    def model_dump(self, *, mode: str = "json") -> dict[str, Any]: ...

    @classmethod
    def model_validate(cls, __data: Any) -> Self: ...


class FlatModel(PydanticModel, Protocol):
    id: str


class AccountScopedModel(PydanticModel, Protocol):
    id: str
    account_id: str


class BaseFlatRepo[TFlat: FlatModel]:
    """Repository for models stored under a single root directory using filename-derived IDs."""

    def __init__(self, file_store: JSONFileStore, root_dir: str, model: type[TFlat]):
        self._file_store = file_store
        self._root_dir = root_dir
        self._model = model

    def get(self, object_id: str) -> TFlat | None:
        data = self._file_store.get(object_id, self._root_dir)
        if data is None:
            return None
        return self._model.model_validate({"id": object_id, **data})

    def list(self, page: int = 1, per_page: int = 10) -> PaginatedList[TFlat]:
        items, total = self._file_store.list(
            self._root_dir,
            page=page,
            per_page=per_page,
        )
        models = [self._model.model_validate(item) for item in items]
        return PaginatedList(items=models, total=total, page=page, per_page=per_page)

    def save(self, model_obj: TFlat) -> TFlat:
        data = model_obj.model_dump(mode="json")
        data.pop("id", None)
        obj_id = model_obj.id
        self._file_store.save(obj_id, data, self._root_dir)
        return model_obj

    def merge_upsert(self, object_id: str, partial: dict[str, object]) -> TFlat:
        existing = self.get(object_id)
        if existing is not None:
            base = existing.model_dump(mode="json")
            base.pop("id", None)
            merged = {**base, **partial}
        else:
            merged = partial
        model_obj = self._model.model_validate({"id": object_id, **merged})
        return self.save(model_obj)


class BaseAccountScopedRepo[TAcct: AccountScopedModel]:
    """Account-scoped models under accounts/<account_id>/<sub_dir>/<id>.json."""

    def __init__(self, file_store: JSONFileStore, sub_dir: str, model: type[TAcct]):
        self._file_store = file_store
        self._sub_dir = sub_dir
        self._model = model

    def get(self, account_id: str, object_id: str) -> TAcct | None:
        data = self._file_store.get(object_id, "accounts", account_id, self._sub_dir)
        if data is None:
            return None
        data.pop("id", None)
        data.pop("account_id", None)
        return self._model.model_validate({"id": object_id, "account_id": account_id, **data})

    def list(self, account_id: str, page: int = 1, per_page: int = 10) -> PaginatedList[TAcct]:
        items, total = self._file_store.list(
            "accounts",
            account_id,
            self._sub_dir,
            page=page,
            per_page=per_page,
        )
        models: list[TAcct] = []
        for item in items:
            file_id = item.get("id")
            item.pop("id", None)
            item.pop("account_id", None)
            models.append(self._model.model_validate({"id": file_id, "account_id": account_id, **item}))
        return PaginatedList(items=models, total=total, page=page, per_page=per_page)

    def save(self, model_obj: TAcct) -> TAcct:
        data = model_obj.model_dump(mode="json")
        for k in ("id", "account_id"):
            data.pop(k, None)
        obj_id = model_obj.id
        acct_id = model_obj.account_id
        self._file_store.save(
            obj_id,
            data,
            "accounts",
            acct_id,
            self._sub_dir,
        )
        return model_obj

    def merge_upsert(self, account_id: str, object_id: str, partial: dict[str, object]) -> TAcct:
        existing = self.get(account_id, object_id)
        if existing is not None:
            base = existing.model_dump(mode="json")
            for k in ("id", "account_id"):
                base.pop(k, None)
            merged = {**base, **partial}
        else:
            merged = partial
        model_obj = self._model.model_validate({"id": object_id, "account_id": account_id, **merged})
        return self.save(model_obj)
