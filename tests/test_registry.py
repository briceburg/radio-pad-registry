def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    # TODO: root is supposed to redirect to /docs ?


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 204
    assert response.content == b""
    assert response.headers.get("cache-control") == "no-store"
