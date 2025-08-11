import multiprocessing
import os
import shutil
import time

import httpx
import pytest
import uvicorn
from starlette.testclient import TestClient

from datastore import DataStore
from lib.constants import BASE_DIR
from models.account import Account
from models.player import Player
from models.station_preset import GlobalStationPreset, Station
from registry import create_app

# Use a consistent, git-ignored directory for test data
TEST_DATA_PATH = BASE_DIR / "data-tests"


@pytest.fixture
def mock_store():
    """
    Fixture to create a clean DataStore for each test, using a dedicated
    /data-tests directory. This ensures test isolation while allowing inspection
    of test data after a run.
    """
    # Clean up and recreate the test data directory for each test
    if TEST_DATA_PATH.exists():
        shutil.rmtree(TEST_DATA_PATH)
    TEST_DATA_PATH.mkdir()

    test_store = DataStore(data_path=str(TEST_DATA_PATH))

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
    shutil.rmtree(TEST_DATA_PATH)


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


def run_server(data_path: str):
    """A simple function to run the Uvicorn server with a specific data path."""
    os.environ["DATA_PATH"] = data_path
    uvicorn.run("registry:app", host="127.0.0.1", port=8000, log_level="warning")


@pytest.fixture(scope="session")
def functional_client(tmp_path_factory):
    """
    A fixture that runs the real server in a separate process, configured to use
    a temporary directory for its data. This allows for testing the application's
    full startup and seeding process.
    """
    data_path = str(tmp_path_factory.mktemp("data"))

    server_process = multiprocessing.Process(target=run_server, args=(data_path,))
    try:
        server_process.start()
        # Wait for the server to be ready by polling the health check endpoint
        max_wait = 5  # seconds
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                with httpx.Client() as client:
                    response = client.get("http://127.0.0.1:8000/healthz")
                    if response.status_code == 200:
                        break
            except httpx.ConnectError:
                time.sleep(0.1)  # Wait a bit before retrying
        else:
            pytest.fail("Server did not start within the specified timeout.")

        yield httpx.Client(base_url="http://127.0.0.1:8000")

    finally:
        # Ensure the server is always terminated, even if assertions fail
        if server_process.is_alive():
            server_process.terminate()
            server_process.join()
