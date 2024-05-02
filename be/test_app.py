import pytest
from app import app


ROOT_NODE_ID = '1'
PARENT_NODE_ID = '2'
CHILD_NODE_ID = '3'


@pytest.fixture
def client():
    return app.test_client()


def test_create_node_missing_name(client):
    data = {'parent_id': 1}
    response = client.post('/create_node', json=data)
    assert response.status_code == 400
    assert 'error' in response.json


def test_create_root_node(client):
    data = {'name': 'Intrepid'}
    response = client.post('/create_node', json=data)
    assert response.status_code == 201
    assert 'id' in response.json


def test_add_property(client):
    data = {'node_id': ROOT_NODE_ID, 'key': 'Mass', 'value': 124.00}
    response = client.post('/add_property', json=data)
    assert response.status_code == 201
    assert 'message' in response.json


def test_create_parent_node(client):
    data = {'name': 'Payload', 'parent_id': ROOT_NODE_ID}
    response = client.post('/create_node', json=data)
    assert response.status_code == 201
    assert 'id' in response.json


def test_create_child_node(client):
    data = {'name': 'DarkMatterCamera', 'parent_id': PARENT_NODE_ID}
    response = client.post('/create_node', json=data)
    assert response.status_code == 201
    assert 'id' in response.json


def test_add_child_node_property(client):
    data = {'node_id': CHILD_NODE_ID, 'key': 'Exposure', 'value': 1.622}
    response = client.post('/add_property', json=data)
    assert response.status_code == 201
    assert 'message' in response.json


def test_get_subtree(client):
    response = client.get('/get_subtree/wrong-path')
    assert response.status_code == 404
    assert 'error' in response.json


def test_get_subtree_valid(client):
    response = client.get('/get_subtree/intrepid')
    json_response = response.json
    assert response.status_code == 200
    assert json_response[0].get('name') == "Intrepid"
