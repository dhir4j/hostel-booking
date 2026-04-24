import hashlib, hmac, json, pytest

def make_sig(secret, body_bytes):
    return hmac.new(secret.encode(), body_bytes, hashlib.sha256).hexdigest()

def test_mock_create_intent(app):
    with app.app_context():
        from app.payments.mock import MockProvider
        p = MockProvider()
        class FakeBooking:
            id = 1
        result = p.create_intent(FakeBooking(), 100, 'INR', {'booking_id': 1})
        assert 'provider_ref' in result
        assert result['status'] == 'pending'

def test_mock_webhook_valid(app):
    with app.app_context():
        from app.payments.mock import MockProvider
        p = MockProvider()
        secret = app.config['WEBHOOK_SECRET']
        payload = {'provider_ref': 'mock_abc', 'status': 'success', 'amount': '500.00'}
        body = json.dumps(payload).encode()
        sig = make_sig(secret, body)
        result = p.verify_webhook({'X-Mock-Signature': sig}, body)
        assert result['provider_ref'] == 'mock_abc'
        assert result['status'] == 'success'

def test_mock_webhook_bad_sig(app):
    with app.app_context():
        from app.payments.mock import MockProvider
        p = MockProvider()
        body = json.dumps({'provider_ref': 'x', 'status': 'success'}).encode()
        with pytest.raises(ValueError):
            p.verify_webhook({'X-Mock-Signature': 'badsig'}, body)
