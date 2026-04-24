import pytest

def test_admin_list_bookings(client, admin_token):
    r = client.get('/api/v1/admin/bookings', headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200
    d = r.get_json()
    assert 'items' in d['data']

def test_approve_nonexistent_booking(client, admin_token):
    r = client.post('/api/v1/admin/bookings/999999/approve',
                    json={}, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 404

def test_reject_nonexistent_booking(client, admin_token):
    r = client.post('/api/v1/admin/bookings/999999/reject',
                    json={}, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 404
