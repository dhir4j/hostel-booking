import time, pytest
from freezegun import freeze_time
from app.utils.tokens import encode_access_token, encode_refresh_token, decode_token, generate_reset_token, hash_token
import jwt

def test_access_token_roundtrip(app):
    with app.app_context():
        token = encode_access_token(42, 'user')
        payload = decode_token(token, expected_type='access')
        assert payload['sub'] == '42'
        assert payload['role'] == 'user'
        assert payload['type'] == 'access'

def test_refresh_token_roundtrip(app):
    with app.app_context():
        token = encode_refresh_token(99)
        payload = decode_token(token, expected_type='refresh')
        assert payload['sub'] == '99'

def test_wrong_type_rejected(app):
    with app.app_context():
        access = encode_access_token(1, 'user')
        with pytest.raises(Exception):
            decode_token(access, expected_type='refresh')

def test_tampered_token_rejected(app):
    with app.app_context():
        token = encode_access_token(1, 'user')
        tampered = token[:-4] + 'XXXX'
        with pytest.raises(Exception):
            decode_token(tampered)

def test_expired_token_rejected(app):
    with app.app_context():
        with freeze_time('2020-01-01'):
            token = encode_access_token(1, 'user')
        with freeze_time('2020-01-02'):
            with pytest.raises(Exception):
                decode_token(token)

def test_reset_token_unique():
    raw1, h1 = generate_reset_token()
    raw2, h2 = generate_reset_token()
    assert raw1 != raw2
    assert h1 != h2

def test_hash_token_consistent():
    raw, h = generate_reset_token()
    assert hash_token(raw) == h
