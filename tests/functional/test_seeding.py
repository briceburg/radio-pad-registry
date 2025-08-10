import pytest


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
