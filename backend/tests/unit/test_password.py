import pytest
from app.utils.password import hash_password, verify_password

def test_hash_returns_string():
    h = hash_password('Secret123!')
    assert isinstance(h, str)
    assert len(h) > 20

def test_verify_correct():
    h = hash_password('Secret123!')
    assert verify_password('Secret123!', h) is True

def test_verify_wrong():
    h = hash_password('Secret123!')
    assert verify_password('Wrong!', h) is False

def test_hash_different_each_time():
    h1 = hash_password('Same')
    h2 = hash_password('Same')
    assert h1 != h2  # bcrypt salt
