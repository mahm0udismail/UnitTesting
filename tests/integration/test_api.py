import pytest
from tests.utils.client import APIClient
from tests.utils.fixtures import test_client
from tests.utils.mock_data import item_data, updated_item_data

@pytest.fixture
def api_client(test_client):
    return APIClient(test_client)

def test_add_item(api_client):
    response = api_client.post("/items", item_data)
    assert response.status_code == 201
    assert response.json["item"]["name"] == item_data["name"]

def test_update_item(api_client):
    post_response = api_client.post("/items", item_data)
    item_id = post_response.json["item"]["id"]

    response = api_client.put(f"/items/{item_id}", updated_item_data)
    assert response.status_code == 200
    assert response.json["item"]["name"] == updated_item_data["name"]

def test_delete_item(api_client):
    post_response = api_client.post("/items", item_data)
    item_id = post_response.json["item"]["id"]

    response = api_client.delete(f"/items/{item_id}")
    assert response.status_code == 200


def test_get_all_items(api_client):
    response = api_client.get("/items")
    assert response.status_code == 200
    data = response.json 
    assert len(data) > 1
    assert data[4]["name"] == "New Item"