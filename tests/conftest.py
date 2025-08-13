import os
import shutil
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from datastore import DataStore
from lib.constants import BASE_DIR
from models.account import Account
from models.player import Player
from models.station_preset import GlobalStationPreset, Station
from registry import create_app


@pytest.fixture(scope="session")
def unit_tests_root() -> Path:
    """Root directory for unit test data under <project>/tmp/tests/unit."""
    root = BASE_DIR / "tmp" / "tests" / "unit"
    root.mkdir(parents=True, exist_ok=True)
    return root


@pytest.fixture
def mock_store(unit_tests_root: Path):
    """
    Fixture to create a clean DataStore for each test, using a dedicated
    tmp/tests/unit/api/data directory. This ensures test isolation while allowing inspection
    of test data after a run.
    """
    data_dir = unit_tests_root / "api" / "data"
    # Clean up and recreate the test data directory for each test
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    test_store = DataStore(data_path=str(data_dir))

    # Pre-populate the store with some consistent test data
    test_store.accounts.save(Account(id="testuser1", name="Test User 1"))
    test_store.accounts.save(Account(id="testuser2", name="Test User 2"))
    test_store.players.save(Player(id="player1", account_id="testuser1", name="Player 1"))
    test_store.players.save(Player(id="player2", account_id="testuser1", name="Player 2"))
    test_store.players.save(Player(id="player3", account_id="testuser2", name="Player 3"))
    test_store.global_presets.save(
        GlobalStationPreset(
            id="briceburg",
            name="Briceburg",
            stations=[
                Station(name="WWOZ", url="https://www.wwoz.org/listen/hi"),
            ],
        )
    )
    yield test_store
    # Clean up the temporary directory after the test
    shutil.rmtree(data_dir)


@pytest.fixture
def client(mock_store):
    app = create_app()

    # Override shared dependency
    from api.dependencies import get_store

    app.dependency_overrides[get_store] = lambda: mock_store

    # Using a `with` statement for the TestClient ensures that the app's
    # lifespan events (startup and shutdown) are correctly triggered.
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client
