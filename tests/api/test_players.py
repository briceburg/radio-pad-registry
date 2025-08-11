import pytest

from tests.api._helpers import assert_item_fields, assert_paginated, get_json, put_json


def test_get_players(client):
    data = get_json(client, "/v1/accounts/testuser1/players")
    assert_paginated(data, total=2)


def test_register_player(client):
    data = put_json(
        client,
        "/v1/accounts/testuser1/players/test-player",
        {"name": "Test Player"},
    )
    assert_item_fields(data, name="Test Player")
    assert "stations_url" in data


def test_register_player_for_new_account(client):
    put_json(
        client,
        "/v1/accounts/new-account/players/test-player",
        {"name": "Test Player"},
    )
    data = get_json(client, "/v1/accounts/new-account/players/test-player")
    assert_item_fields(data, name="Test Player")
    accounts = get_json(client, "/v1/accounts")
    assert "new-account" in [item["id"] for item in accounts["items"]]


def test_update_player(client):
    put_json(
        client,
        "/v1/accounts/testuser1/players/player1",
        {"name": "Updated Player"},
    )
    data = get_json(client, "/v1/accounts/testuser1/players/player1")
    assert_item_fields(data, name="Updated Player")


def test_get_player_not_found(client):
    get_json(client, "/v1/accounts/testuser1/players/does-not-exist", expected=404)


def test_update_player_preserves_existing_data(client):
    original_stations_url = "https://original.url/stations.json"
    put_json(
        client,
        "/v1/accounts/testuser1/players/player1",
        {"name": "Player 1", "stations_url": original_stations_url},
    )

    put_data = put_json(
        client,
        "/v1/accounts/testuser1/players/player1",
        {"name": "Updated Player Name"},
    )
    assert_item_fields(
        put_data,
        name="Updated Player Name",
        stations_url=original_stations_url,
    )

    get_data = get_json(client, "/v1/accounts/testuser1/players/player1")
    assert_item_fields(
        get_data,
        name="Updated Player Name",
        stations_url=original_stations_url,
    )


@pytest.mark.parametrize(
    "body,expect_status",
    [
        ({"name": "Valid Player"}, 200),
        ({}, 422),  # missing required name
    ],
)
def test_player_create_validation(client, body, expect_status):
    resp = client.put("/v1/accounts/testuser1/players/param-player", json=body)
    assert resp.status_code == expect_status
    if expect_status == 200:
        assert resp.json()["name"] == body["name"]
    else:
        assert resp.json()["detail"]


@pytest.mark.parametrize(
    "invalid_id",
    [
        "Invalid",  # uppercase first letter
        "has space",
        "UPPER",
        "mixedCase",
        "trailing-",
        "-leading",
        "bad_id",  # underscore
        "bad--id",  # double dash
    ],
)
def test_player_invalid_id_rejected(client, invalid_id):
    resp = client.put(
        f"/v1/accounts/testuser1/players/{invalid_id}",
        json={"name": "Bad"},
    )
    assert resp.status_code == 422


# New: invalid account_id path segment should 422 before hitting model logic
@pytest.mark.parametrize(
    "invalid_account_id",
    [
        "BadAcct",
        "bad acct",
        "acct_1",
        "acct--1",
        "-acct",
        "acct-",
    ],
)
def test_player_invalid_account_id_rejected(client, invalid_account_id):
    resp = client.put(
        f"/v1/accounts/{invalid_account_id}/players/playerx",
        json={"name": "X"},
    )
    assert resp.status_code == 422


# Positive edge-case slugs should work
@pytest.mark.parametrize(
    "account_id,player_id",
    [
        ("a", "a"),
        ("abc", "abc-def"),
        ("abc-def-123", "player-123"),
    ],
)
def test_player_valid_slug_edge_cases(client, account_id, player_id):
    resp = client.put(
        f"/v1/accounts/{account_id}/players/{player_id}",
        json={"name": "Edge"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == player_id
    assert data["account_id"] == account_id


def test_player_partial_update_preserves_unspecified_fields(client):
    """Create a player with optional fields then update only name; optional fields must persist."""
    account_id = "testuser1"
    player_id = "partial-player"
    initial = {
        "name": "Original Name",
        "stations_url": "https://example.com/custom.json",
        "switchboard_url": "wss://switch.example.com/custom",
    }
    created = put_json(
        client,
        f"/v1/accounts/{account_id}/players/{player_id}",
        initial,
    )
    assert_item_fields(
        created,
        id=player_id,
        name="Original Name",
        stations_url=initial["stations_url"],
        switchboard_url=initial["switchboard_url"],
    )

    # Now update only the name
    updated = put_json(
        client,
        f"/v1/accounts/{account_id}/players/{player_id}",
        {"name": "Renamed"},
    )
    assert_item_fields(
        updated,
        id=player_id,
        name="Renamed",
        stations_url=initial["stations_url"],
        switchboard_url=initial["switchboard_url"],
    )

    # Fetch again to ensure persistence
    fetched = get_json(
        client,
        f"/v1/accounts/{account_id}/players/{player_id}",
    )
    assert_item_fields(
        fetched,
        id=player_id,
        name="Renamed",
        stations_url=initial["stations_url"],
        switchboard_url=initial["switchboard_url"],
    )
