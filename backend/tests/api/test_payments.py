import hashlib, hmac, json, pytest

def test_create_intent_unauthenticated(client):
    r = client.post('/api/v1/payments/create-intent', json={'booking_id': 1})
    assert r.status_code == 401

def test_create_intent_nonexistent_booking(client, user_token):
    r = client.post('/api/v1/payments/create-intent',
                    json={'booking_id': 999999},
                    headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 404

def test_webhook_bad_signature(client, app):
    body = json.dumps({'provider_ref': 'x', 'status': 'success'}).encode()
    r = client.post('/api/v1/payments/webhook/mock',
                    data=body,
                    content_type='application/json',
                    headers={'X-Mock-Signature': 'badsignature'})
    assert r.status_code == 400

def test_webhook_valid_signature(client, app):
    secret = app.config['WEBHOOK_SECRET']
    payload = {'provider_ref': 'mock_testref123', 'status': 'success', 'amount': '100.00'}
    body = json.dumps(payload).encode()
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    r = client.post('/api/v1/payments/webhook/mock',
                    data=body,
                    content_type='application/json',
                    headers={'X-Mock-Signature': sig})
    # 200 even if booking not found (payment has no booking_id in this case)
    assert r.status_code == 200
