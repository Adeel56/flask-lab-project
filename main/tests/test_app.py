import json
from app import app

def test_home():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Flask Lab Project" in resp.data

def test_health():
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert b"OK" in resp.data

def test_post_data_json():
    client = app.test_client()
    data = {"name": "test"}
    resp = client.post('/data', json=data)
    assert resp.status_code == 200
    body = resp.get_json()
    assert "received" in body
    assert body["received"]["name"] == "test"

def test_post_data_non_json():
    client = app.test_client()
    resp = client.post('/data', data="not json", headers={"Content-Type":"text/plain"})
    assert resp.status_code == 400
