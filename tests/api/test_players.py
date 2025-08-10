from models.player import Player


def test_get_players(client):
    response = client.get("/v1/accounts/testuser1/players")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "per_page" in data
    assert "total" in data
    assert data["total"] == 2
    assert isinstance(data["items"], list)


def test_register_player(client):
    response = client.put(
        "/v1/accounts/testuser1/players/test-player", json={"name": "Test Player"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Player"
    assert "stations_url" in data


def test_register_player_for_new_account(client):
    response = client.put(
        "/v1/accounts/new-account/players/test-player", json={"name": "Test Player"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Player"

    response = client.get("/v1/accounts/new-account/players/test-player")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Player"

    response = client.get("/v1/accounts")
    assert response.status_code == 200
    data = response.json()
    assert "new-account" in [item["id"] for item in data["items"]]


def test_update_player(client):
    response = client.put(
        "/v1/accounts/testuser1/players/player1", json={"name": "Updated Player"}
    )
    print('DEBUG update response', response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Player"

    response = client.get("/v1/accounts/testuser1/players/player1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Player"


def test_get_player_not_found(client):
    response = client.get("/v1/accounts/testuser1/players/does-not-exist")
    assert response.status_code == 404


def test_update_player_preserves_existing_data(client):
    original_stations_url = "https://original.url/stations.json"
    # Seed existing data through API (PUT ensures creation)
    client.put(
        "/v1/accounts/testuser1/players/player1",
        json={"name": "Player 1", "stations_url": original_stations_url},
    )

    response = client.put(
        "/v1/accounts/testuser1/players/player1", json={"name": "Updated Player Name"}
    )
    assert response.status_code == 200
    put_data = response.json()
    assert put_data["name"] == "Updated Player Name"
    assert put_data["stations_url"] == original_stations_url

    response = client.get("/v1/accounts/testuser1/players/player1")
    assert response.status_code == 200
    get_data = response.json()
    assert get_data["name"] == "Updated Player Name"
    assert get_data["stations_url"] == original_stations_url