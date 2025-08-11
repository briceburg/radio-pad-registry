import json

import pytest
from starlette.testclient import TestClient

from registry import create_app


@pytest.mark.functional
def test_seeded_account_is_loaded(functional_client):
    """
    A functional test to verify that the seed data for accounts is loaded
    correctly on application startup.
    """
    response = functional_client.get("/v1/accounts")
    assert response.status_code == 200
    data = response.json()
    assert "briceburg" in [item["id"] for item in data["items"]]


@pytest.mark.functional
def test_seeded_player_is_loaded(functional_client):
    """
    A functional test to verify that the seed data for players is loaded
    correctly on application startup.
    """
    response = functional_client.get("/v1/accounts/briceburg/players")
    assert response.status_code == 200
    data = response.json()
    assert "living-room" in [item["id"] for item in data["items"]]


@pytest.mark.functional
def test_seeded_global_preset_is_loaded(functional_client):
    """
    A functional test to verify that the seed data for global presets is loaded
    correctly on application startup.
    """
    response = functional_client.get("/v1/presets")
    assert response.status_code == 200
    data = response.json()
    assert "briceburg" in [item["id"] for item in data["items"]]


@pytest.mark.functional
def test_custom_seed_idempotency(tmp_path, monkeypatch):
    """Start app with custom seed dir, verify copy then idempotent on restart."""
    seed_dir = tmp_path / "seed"
    (seed_dir / "accounts").mkdir(parents=True)
    (seed_dir / "presets").mkdir(parents=True)
    (seed_dir / "accounts" / "acct-seeded.json").write_text(json.dumps({"name": "Seeded Account"}))
    (seed_dir / "presets" / "jazz.json").write_text(json.dumps({"name": "Jazz", "stations": []}))

    data_dir = tmp_path / "data"
    monkeypatch.setenv("DATA_PATH", str(data_dir))
    monkeypatch.setenv("SEED_PATH", str(seed_dir))

    app = create_app()
    with TestClient(app) as client:
        accounts = client.get("/v1/accounts").json()
        assert any(a["id"] == "acct-seeded" for a in accounts["items"])
        presets = client.get("/v1/presets").json()
        assert any(p["id"] == "jazz" for p in presets["items"])

    acct_file = data_dir / "accounts" / "acct-seeded.json"
    acct_file.write_text(json.dumps({"name": "Modified"}))

    app2 = create_app()
    with TestClient(app2) as client:
        accounts2 = client.get("/v1/accounts").json()
        assert any(a["id"] == "acct-seeded" for a in accounts2["items"])
        assert acct_file.read_text() == json.dumps({"name": "Modified"})
    assert (data_dir / "presets" / "jazz.json").is_file()
