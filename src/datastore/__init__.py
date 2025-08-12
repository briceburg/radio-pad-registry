from pathlib import Path

from lib.constants import BASE_DIR
from lib.logging import logger

from .accounts import Accounts
from .backends.json_file_store import JSONFileStore
from .model_store import ModelStore
from .players import Players
from .presets import AccountPresets, GlobalPresets


class DataStore:
    """A container for the application's data stores."""

    def __init__(self, data_path: str | None = None, seed_path: str | None = None) -> None:
        # Provide sensible defaults so tests can construct without args
        self.data_path = Path(data_path) if data_path else BASE_DIR / "tmp" / "data"
        self.seed_path = Path(seed_path) if seed_path else BASE_DIR / "data"
        self.file_store = JSONFileStore(str(self.data_path))
        self.accounts = Accounts(self.file_store)
        self.players = Players(self.file_store)
        self.global_presets = GlobalPresets(self.file_store)
        self.account_presets = AccountPresets(self.file_store)

    def seed(self) -> None:
        """
        Seeds the datastore with initial data from the data-seed directory.
        Only seeds data if it doesn't already exist in the target datastore.
        """
        import os
        import shutil

        if not self.seed_path.is_dir():
            logger.error(f"Seed path does not exist: {self.seed_path}")
            return

        for dirpath, _, filenames in os.walk(self.seed_path):
            for filename in filenames:
                if not filename.endswith(".json"):
                    continue
                seed_file = Path(dirpath) / filename
                target_file = self.data_path / seed_file.relative_to(self.seed_path)
                if not target_file.exists():
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(seed_file, target_file)
                    logger.info(f"Seeded {target_file}")


__all__ = [
    "AccountPresets",
    "Accounts",
    "DataStore",
    "GlobalPresets",
    "JSONFileStore",
    "ModelStore",
    "Players",
]
