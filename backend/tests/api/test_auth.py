import pytest

BASE = '/api/v1/auth'

def test_register_success(client):
    r = client.post(f'{BASE}/register', json={
        'full_name': 'Test User', 'email': 'new@test.com', 'password': 'Password1!'
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data['success'] is True
    assert 'user' in data['data']
    assert 'password_hash' not in str(data)

def test_register_duplicate_email(client):
    payload = {'full_name': 'X', 'email': 'dup@test.com', 'password': 'Password1!'}
    client.post(f'{BASE}/register', json=payload)
    r = client.post(f'{BASE}/register', json=payload)
    assert r.status_code in (400, 409)

def test_register_weak_password(client):
    r = client.post(f'{BASE}/register', json={
        'full_name': 'X', 'email': 'weak@test.com', 'password': '123'
    })
    assert r.status_code == 400

def test_login_success(client):
    client.post(f'{BASE}/register', json={
        'full_name': 'Login Test', 'email': 'login@test.com', 'password': 'Password1!'
    })
    r = client.post(f'{BASE}/login', json={'email': 'login@test.com', 'password': 'Password1!'})
    assert r.status_code == 200
    assert 'access_token' in r.get_json()['data']

def test_login_wrong_password(client):
    r = client.post(f'{BASE}/login', json={'email': 'x@x.com', 'password': 'wrong'})
    assert r.status_code == 401

def test_forgot_password_always_200(client):
    r = client.post(f'{BASE}/forgot-password', json={'email': 'nonexistent@test.com'})
    assert r.status_code == 200
    assert r.get_json()['success'] is True

def test_reset_password_bad_token(client):
    r = client.post(f'{BASE}/reset-password', json={'token': 'badtoken', 'new_password': 'NewPass1!'})
    assert r.status_code == 400
