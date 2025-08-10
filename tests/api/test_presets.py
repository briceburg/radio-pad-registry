import pytest


def test_list_global_presets(client):
    """Test listing global station presets."""
    response = client.get("/v1/presets")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 0
    assert "items" in data


def test_get_global_preset(client):
    """Test getting a single global station preset by ID."""
    # First, create a preset to get
    preset_id = "test-preset"
    preset_data = {
        "name": "Test Preset",
        "stations": [{"name": "A", "url": "https://a.com"}],
    }
    client.put(f"/v1/presets/{preset_id}", json=preset_data)

    response = client.get(f"/v1/presets/{preset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == preset_id
    assert "stations" in data


def test_get_global_preset_not_found(client):
    """Test getting a non-existent global station preset."""
    response = client.get("/v1/presets/does-not-exist")
    assert response.status_code == 404


def test_register_global_preset(client):
    """Test creating a new global station preset with all fields."""
    preset_id = "new-global-preset"
    preset_data = {
        "name": "New Global Preset",
        "category": "News",
        "description": "A collection of news stations.",
        "stations": [
            {"name": "A Cool Station", "url": "https://cool.station/stream"},
        ],
    }
    response = client.put(f"/v1/presets/{preset_id}", json=preset_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == preset_id
    assert data["name"] == "New Global Preset"
    assert data["category"] == "News"
    assert data["description"] == "A collection of news stations."
    assert "account_id" not in data


def test_register_global_preset_missing_optional_fields(client):
    """Test creating a preset works when optional fields are missing."""
    preset_id = "minimal-preset"
    preset_data = {
        "name": "Minimal Preset",
        "stations": [],
    }
    response = client.put(f"/v1/presets/{preset_id}", json=preset_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Minimal Preset"
    assert data.get("category") is None
    assert data.get("description") is None


@pytest.mark.parametrize(
    "missing_field",
    ["name", "stations"],
)
def test_register_global_preset_missing_required_field(client, missing_field):
    """Test that creating a preset fails if required fields are missing."""
    preset_id = "invalid-preset"
    preset_data = {
        "name": "Invalid Preset",
        "stations": [],
    }
    del preset_data[missing_field]
    response = client.put(f"/v1/presets/{preset_id}", json=preset_data)
    assert response.status_code == 422
