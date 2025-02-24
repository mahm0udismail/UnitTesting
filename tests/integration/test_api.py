import pytest
from tests.utils.client import APIClient
from tests.utils.fixtures import test_client
from tests.utils.mock_data import (item_data, 
                                   updated_item_data,
                                   invalid_item_data_missing_name,
                                   invalid_item_data_empty_name
                                   )

@pytest.fixture
def api_client(test_client):
    return APIClient(test_client)

def test_add_item(api_client):
    response = api_client.post("/items", item_data)
    assert response.status_code == 201
    assert response.json["item"]["name"] == item_data["name"]

@pytest.mark.parametrize(
    "payload, expected_status, expected_message",
    [
        (item_data, 201, "New Item"),  
        (invalid_item_data_missing_name, 400, "Invalid data"),  
        (None, 400, "Invalid data"),
    ]
)


def test_add_item(api_client, payload, expected_status, expected_message):
    response = api_client.post("/items", payload)
    
    assert response.status_code == expected_status
    
    if expected_status == 201:  # Success case
        assert response.json["item"]["name"] == expected_message
    else:  # Error case
        assert response.json["error"] == expected_message

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