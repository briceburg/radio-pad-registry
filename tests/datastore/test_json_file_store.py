import json
import os
from pathlib import Path

import pytest

from datastore.backends.json_file_store import JSONFileStore


@pytest.fixture
def file_store(tmp_path: Path) -> JSONFileStore:
    return JSONFileStore(str(tmp_path))


def test_save_and_get(file_store: JSONFileStore):
    object_id = "test-object"
    data = {"key": "value"}
    path_parts = ("test", "path")
    file_store.save(object_id, data, *path_parts)
    retrieved_data = file_store.get(object_id, *path_parts)
    assert retrieved_data == data


def test_get_non_existent(file_store: JSONFileStore):
    retrieved_data = file_store.get("non-existent", "test", "path")
    assert retrieved_data is None


def test_list(file_store: JSONFileStore):
    path_parts = ("test", "list")
    for i in range(15):
        file_store.save(f"obj-{i:02}", {"id": i}, *path_parts)
    items, total = file_store.list(*path_parts, page=1, per_page=10)
    assert total == 15
    assert len(items) == 10
    assert items[0]["id"] == "obj-00"
    assert items[9]["id"] == "obj-09"
    items, total = file_store.list(*path_parts, page=2, per_page=10)
    assert total == 15
    assert len(items) == 5
    assert items[0]["id"] == "obj-10"
    assert items[4]["id"] == "obj-14"


def test_delete(file_store: JSONFileStore):
    object_id = "test-object"
    path_parts = ("test", "delete")
    file_store.save(object_id, {"key": "value"}, *path_parts)
    assert file_store.get(object_id, *path_parts) is not None
    deleted = file_store.delete(object_id, *path_parts)
    assert deleted is True
    assert file_store.get(object_id, *path_parts) is None


def test_delete_non_existent(file_store: JSONFileStore):
    deleted = file_store.delete("non-existent", "test", "delete")
    assert deleted is False