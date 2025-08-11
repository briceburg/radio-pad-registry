import json
import os
from glob import glob
from pathlib import Path
from typing import Any, cast

from lib.types import PagedResult


class JSONFileStore:
    """A file-based store for JSON data."""

    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_path(self, *parts: str) -> Path:
        """Constructs a path relative to the base path."""
        return self.base_path.joinpath(*parts)

    def get(self, object_id: str, *path_parts: str) -> dict[str, Any] | None:
        """
        Retrieves a JSON object by its ID from a specified path.
        """
        file_path = self._get_path(*path_parts, f"{object_id}.json")
        if not file_path.exists():
            return None
        with open(file_path) as f:
            data = cast(dict[str, Any], json.load(f))
        return data

    def list(self, *path_parts: str, page: int = 1, per_page: int = 10) -> PagedResult[dict[str, Any]]:
        """
        Lists JSON objects from a specified path with pagination.
        The 'id' of each object is derived from its filename if not present in the file.
        """
        directory = self._get_path(*path_parts)
        if not directory.exists():
            return [], 0

        file_paths = sorted(glob(f"{directory}/*.json"))
        total = len(file_paths)

        start = (page - 1) * per_page
        end = start + per_page
        paginated_paths = file_paths[start:end]

        items: list[dict[str, Any]] = []
        for file_path in paginated_paths:
            with open(file_path) as f:
                item = cast(dict[str, Any], json.load(f))
                # Always derive id from filename; exclude any stored id field
                item["id"] = Path(file_path).stem
                items.append(item)

        return items, total

    def save(self, object_id: str, data: dict[str, Any], *path_parts: str) -> None:
        """
        Saves a JSON object by its ID to a specified path.
        Keeps any explicit 'id' field provided by caller.
        """
        directory = self._get_path(*path_parts)
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory.joinpath(f"{object_id}.json")

        # Strip id field prior to persistence
        data_to_save = {k: v for k, v in data.items() if k != "id"}
        with open(file_path, "w") as f:
            json.dump(data_to_save, f, indent=2)

    def delete(self, object_id: str, *path_parts: str) -> bool:
        """
        Deletes a JSON object by its ID from a specified path.
        Returns True if the object was deleted, False otherwise.
        """
        file_path = self._get_path(*path_parts, f"{object_id}.json")
        if not file_path.exists():
            return False
        os.remove(file_path)
        return True

    def patch(self, object_id: str, patch_data: dict[str, Any], *path_parts: str) -> None:
        """
        Applies a partial update to a JSON object.
        """
        file_path = self._get_path(*path_parts, f"{object_id}.json")
        if file_path.exists():
            with open(file_path, "r+") as f:
                data = cast(dict[str, Any], json.load(f))
                data.update({k: v for k, v in patch_data.items() if k != "id"})
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        else:
            # If the object doesn't exist, create it with the patch data.
            self.save(object_id, patch_data, *path_parts)
