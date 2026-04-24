import pytest

def _create_hostel_and_room(client, admin_token):
    """Helper: create hostel + room, return (hostel_id, room_id)."""
    h = client.post('/api/v1/admin/hostels', json={
        'name': 'Test Hostel', 'city': 'Mumbai', 'address': '123 Main St'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    hostel_id = h.get_json()['data']['hostel']['id']
    r = client.post('/api/v1/admin/rooms', json={
        'hostel_id': hostel_id, 'room_number': '101',
        'capacity': 2, 'price_per_night': '500.00'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    room_id = r.get_json()['data']['room']['id']
    return hostel_id, room_id

def test_create_booking_unauthenticated(client):
    r = client.post('/api/v1/bookings', json={})
    assert r.status_code == 401

def test_list_my_bookings(client, user_token):
    r = client.get('/api/v1/bookings/my', headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 200
    assert 'items' in r.get_json()['data']

def test_create_booking_invalid_dates(client, user_token, admin_token):
    hostel_id, room_id = _create_hostel_and_room(client, admin_token)
    r = client.post('/api/v1/bookings', json={
        'hostel_id': hostel_id, 'room_id': room_id,
        'check_in': '2025-01-10', 'check_out': '2025-01-05',  # reversed
        'guests_count': 1
    }, headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code in (400, 422)
