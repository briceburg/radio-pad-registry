import pytest
from fastapi import status

from models.pagination import PaginatedList
from tests.api._helpers import get_json, put_json


@pytest.mark.parametrize(
    "url,total",
    [
        ("/v1/accounts", 2),
        ("/v1/accounts/testuser1/players", 2),
        ("/v1/presets", 1),
    ],
)
def test_pagination_out_of_bounds(client, url: str, total: int):
    data = get_json(client, f"{url}?page=1000&per_page=1")
    assert len(data["items"]) == 0
    assert data["page"] == 1000
    assert data["per_page"] == 1
    assert data["total"] == total
    assert data["has_prev"] is True  # because page > 1
    assert data["has_next"] is False


@pytest.mark.parametrize(
    "url,total",
    [
        ("/v1/accounts", 2),
        ("/v1/accounts/testuser1/players", 2),
        ("/v1/presets", 1),
    ],
)
def test_per_page_parameter_works(client, url: str, total: int):
    data = get_json(client, f"{url}?page=1&per_page={total}")
    assert len(data["items"]) == total
    assert data["page"] == 1
    assert data["per_page"] == total
    assert data["total"] == total
    assert data["has_prev"] is False

    data = get_json(client, f"{url}?page=1&per_page={total + 1}")
    assert len(data["items"]) == total
    assert data["page"] == 1
    assert data["per_page"] == total + 1
    assert data["total"] == total
    assert data["has_prev"] is False


@pytest.mark.parametrize(
    "url,item_id_1,item_id_2,total",
    [
        ("/v1/accounts", "testuser1", "testuser2", 2),
        ("/v1/accounts/testuser1/players", "player1", "player2", 2),
    ],
)
def test_pagination_works(client, url: str, item_id_1: str, item_id_2: str, total: int):
    data = get_json(client, f"{url}?page=1&per_page=1")
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == item_id_1
    assert data["page"] == 1
    assert data["per_page"] == 1
    assert data["total"] == total
    assert data["has_prev"] is False
    assert data["has_next"] is (total > 1)

    data = get_json(client, f"{url}?page=2&per_page=1")
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == item_id_2
    assert data["page"] == 2
    assert data["per_page"] == 1
    assert data["total"] == total
    assert data["has_prev"] is True


# Unit-style tests for PaginatedList metadata (model-level)


def test_paginated_list_middle_page():
    pl = PaginatedList(items=[1, 2, 3], total=25, page=2, per_page=10)
    assert pl.pages == 3
    assert pl.has_prev is True
    assert pl.has_next is True
    assert pl.prev_page == 1
    assert pl.next_page == 3


def test_paginated_list_first_page():
    pl = PaginatedList(items=[1, 2], total=23, page=1, per_page=10)
    assert pl.pages == 3
    assert pl.has_prev is False
    assert pl.prev_page is None
    assert pl.has_next is True
    assert pl.next_page == 2


def test_paginated_list_last_partial_page():
    pl = PaginatedList(items=[1, 2, 3], total=23, page=3, per_page=10)
    assert pl.pages == 3
    assert pl.has_next is False
    assert pl.next_page is None
    assert pl.has_prev is True
    assert pl.prev_page == 2


def test_paginated_list_exact_division_last_page():
    pl = PaginatedList(items=[1], total=30, page=3, per_page=10)
    assert pl.pages == 3
    assert pl.has_next is False
    assert pl.has_prev is True


def test_paginated_list_single_page():
    pl = PaginatedList(items=[1, 2, 3], total=3, page=1, per_page=10)
    assert pl.pages == 1
    assert pl.has_next is False
    assert pl.has_prev is False
    assert pl.next_page is None
    assert pl.prev_page is None


@pytest.mark.parametrize(
    "raw_page,raw_per",
    [
        (0, 10),  # page too low
        (-1, 5),  # negative page
        (1, 0),  # per_page too low
        (1, 101),  # per_page too high (beyond max)
    ],
)
def test_pagination_invalid_values_rejected(client, raw_page, raw_per):
    resp = client.get(f"/v1/accounts?page={raw_page}&per_page={raw_per}")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = resp.json()["detail"]
    assert detail


def test_large_dataset_pagination_players(client):
    account = "bulkacct"
    # create 23 players -> p00 .. p22
    for i in range(23):
        pid = f"p{i:02d}"
        put_json(client, f"/v1/accounts/{account}/players/{pid}", {"name": f"Player {i}"})

    # Page 1
    page1 = get_json(client, f"/v1/accounts/{account}/players?page=1&per_page=10")
    assert page1["total"] == 23
    assert len(page1["items"]) == 10
    assert page1["items"][0]["id"] == "p00"
    assert page1["items"][-1]["id"] == "p09"
    assert page1["has_prev"] is False
    assert page1["has_next"] is True
    assert page1["pages"] == 3

    # Page 2
    page2 = get_json(client, f"/v1/accounts/{account}/players?page=2&per_page=10")
    assert len(page2["items"]) == 10
    assert page2["items"][0]["id"] == "p10"
    assert page2["items"][-1]["id"] == "p19"
    assert page2["has_prev"] is True
    assert page2["has_next"] is True

    # Deterministic ordering (repeat page 2)
    page2_repeat = get_json(client, f"/v1/accounts/{account}/players?page=2&per_page=10")
    assert [p["id"] for p in page2_repeat["items"]] == [p["id"] for p in page2["items"]]

    # Page 3 (last partial)
    page3 = get_json(client, f"/v1/accounts/{account}/players?page=3&per_page=10")
    assert len(page3["items"]) == 3
    assert [p["id"] for p in page3["items"]] == ["p20", "p21", "p22"]
    assert page3["has_prev"] is True
    assert page3["has_next"] is False
