import pytest

BASE = '/api/v1/admin'

def test_create_hostel(client, admin_token):
    r = client.post(f'{BASE}/hostels', json={
        'name': 'My Hostel', 'city': 'Delhi', 'address': '1 Main Rd'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 201
    d = r.get_json()['data']
    assert d['hostel']['name'] == 'My Hostel'

def test_create_hostel_missing_fields(client, admin_token):
    r = client.post(f'{BASE}/hostels', json={'name': 'X'},
                    headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 400

def test_list_hostels_admin(client, admin_token):
    r = client.get(f'{BASE}/hostels', headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200

def test_create_room(client, admin_token):
    h = client.post(f'{BASE}/hostels', json={
        'name': 'Room Test', 'city': 'Pune', 'address': '5 Street'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    hostel_id = h.get_json()['data']['hostel']['id']
    r = client.post(f'{BASE}/rooms', json={
        'hostel_id': hostel_id, 'room_number': 'A1', 'capacity': 4, 'price_per_night': '750.00'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 201
    assert r.get_json()['data']['room']['room_number'] == 'A1'
