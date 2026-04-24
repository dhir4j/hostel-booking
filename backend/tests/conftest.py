import os
import pytest
os.environ.setdefault('APP_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret-key-32bytes!!!!!')
os.environ.setdefault('DATABASE_URL', os.environ.get('TEST_DATABASE_URL', 'postgresql://localhost/hostel_test'))
os.environ.setdefault('INTERNAL_API_KEY', 'test-internal-key')
os.environ.setdefault('WEBHOOK_SECRET', 'test-webhook-secret')
os.environ.setdefault('FRONTEND_URL', 'http://localhost:3000')

from app import create_app
from app.extensions import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(autouse=True)
def db_rollback(db):
    """Roll back each test in a savepoint."""
    connection = db.engine.connect()
    transaction = connection.begin()
    # Bind session to this connection
    db.session.bind = connection
    nested = connection.begin_nested()
    yield
    db.session.remove()
    nested.rollback()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(db, app):
    from app.models.user import User
    from app.utils.password import hash_password
    with app.app_context():
        u = User(full_name='Admin User', email='admin@test.com',
                 password_hash=hash_password('Admin1234!'), role='admin', is_active=True)
        db.session.add(u)
        db.session.flush()
        return u

@pytest.fixture
def regular_user(db, app):
    from app.models.user import User
    from app.utils.password import hash_password
    with app.app_context():
        u = User(full_name='Regular User', email='user@test.com',
                 password_hash=hash_password('User1234!'), role='user', is_active=True)
        db.session.add(u)
        db.session.flush()
        return u

@pytest.fixture
def admin_token(app, admin_user):
    with app.app_context():
        from app.utils.tokens import encode_access_token
        return encode_access_token(admin_user.id, 'admin')

@pytest.fixture
def user_token(app, regular_user):
    with app.app_context():
        from app.utils.tokens import encode_access_token
        return encode_access_token(regular_user.id, 'user')

def auth_headers(token):
    return {'Authorization': f'Bearer {token}'}
