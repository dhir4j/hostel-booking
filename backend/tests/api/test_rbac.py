import pytest

def test_admin_hostels_requires_auth(client):
    r = client.get('/api/v1/admin/hostels')
    assert r.status_code == 401

def test_admin_hostels_requires_admin_role(client, user_token):
    r = client.get('/api/v1/admin/hostels', headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 403

def test_admin_hostels_admin_allowed(client, admin_token):
    r = client.get('/api/v1/admin/hostels', headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200

def test_admin_bookings_requires_auth(client):
    r = client.get('/api/v1/admin/bookings')
    assert r.status_code == 401

def test_admin_analytics_requires_admin(client, user_token):
    r = client.get('/api/v1/admin/analytics/summary', headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 403

def test_users_me_requires_auth(client):
    r = client.get('/api/v1/users/me')
    assert r.status_code == 401

def test_users_me_with_token(client, user_token):
    r = client.get('/api/v1/users/me', headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 200

def test_internal_requires_key(client):
    r = client.post('/api/v1/internal/expire-holds')
    assert r.status_code == 401

def test_internal_with_key(client, app):
    key = app.config['INTERNAL_API_KEY']
    r = client.post('/api/v1/internal/expire-holds', headers={'X-Internal-API-Key': key})
    assert r.status_code == 200

def test_healthz_public(client):
    r = client.get('/api/v1/healthz')
    assert r.status_code == 200
