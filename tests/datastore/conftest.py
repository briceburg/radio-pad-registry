import shutil
import uuid
from pathlib import Path

import pytest

from datastore import DataStore
from lib.constants import BASE_DIR


@pytest.fixture
def temp_data_path() -> Path:
    """Provide a stable project-level temporary data directory for datastore tests.
    Uses <project>/tmp/tests/data (gitignored) so artifacts are inspectable after runs.
    Cleaned before each use for isolation.
    """
    base = BASE_DIR / "tmp" / "tests" / "data"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True, exist_ok=True)
    return base


@pytest.fixture
def datastore_factory():
    """Factory to create isolated DataStore instances under <project>/tmp/tests/stores/<uuid>."""
    root_base = BASE_DIR / "tmp" / "tests" / "stores"
    root_base.mkdir(parents=True, exist_ok=True)

    def _make(**kwargs):
        store_root = root_base / uuid.uuid4().hex
        store_root.mkdir()
        return DataStore(data_path=str(store_root), **kwargs)

    return _make
