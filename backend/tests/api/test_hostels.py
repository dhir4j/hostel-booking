import pytest

BASE = '/api/v1'

def test_list_hostels_public(client):
    r = client.get(f'{BASE}/hostels')
    assert r.status_code == 200
    d = r.get_json()
    assert d['success'] is True
    assert 'items' in d['data']

def test_list_hostels_pagination(client):
    r = client.get(f'{BASE}/hostels?page=1&per_page=5')
    assert r.status_code == 200

def test_get_hostel_not_found(client):
    r = client.get(f'{BASE}/hostels/999999')
    assert r.status_code == 404

def test_response_envelope_shape(client):
    r = client.get(f'{BASE}/hostels')
    d = r.get_json()
    assert 'success' in d
    assert 'data' in d
    assert 'error' in d
    assert 'meta' in d
