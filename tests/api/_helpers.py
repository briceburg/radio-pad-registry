def put_json(client, path: str, body: dict, expected: int = 200) -> dict:
    resp = client.put(path, json=body)
    assert resp.status_code == expected, f"expected {expected} got {resp.status_code}: {resp.text}"
    if expected == 200:
        return resp.json()
    return {}


def get_json(client, path: str, expected: int = 200) -> dict:
    resp = client.get(path)
    assert resp.status_code == expected, f"GET {path} expected {expected} got {resp.status_code}: {resp.text}"
    if expected == 200:
        return resp.json()
    return {}


def assert_paginated(payload: dict, total: int | None = None):
    for key in ("items", "total", "page", "per_page"):
        assert key in payload, f"Missing pagination key {key}"
    if total is not None:
        assert payload["total"] == total


def assert_item_fields(item: dict, **expected):
    for k, v in expected.items():
        assert item.get(k) == v, f"Field {k} expected {v} got {item.get(k)}"
