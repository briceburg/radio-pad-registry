def test_get_players(client):
    response = client.get("/v1/players")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "per_page" in data
    assert "total" in data
    assert "total_pages" in data
    assert isinstance(data["items"], list)


# TODO: add preset fixtures to further exercise. check for 404s.
