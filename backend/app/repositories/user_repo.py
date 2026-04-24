from app.extensions import db
from app.models.user import User, AdminProfile


def get_by_id(user_id: int) -> User | None:
    return db.session.get(User, user_id)


def get_by_email(email: str) -> User | None:
    from sqlalchemy import select
    return db.session.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()


def create(full_name: str, email: str, password_hash: str, phone: str | None = None, role: str = 'user') -> User:
    user = User(full_name=full_name, email=email.lower(), password_hash=password_hash, phone=phone, role=role)
    db.session.add(user)
    db.session.flush()
    return user


def update(user: User, **kwargs) -> User:
    for k, v in kwargs.items():
        setattr(user, k, v)
    db.session.flush()
    return user


def email_exists(email: str) -> bool:
    from sqlalchemy import select, exists
    return db.session.execute(select(exists().where(User.email == email.lower()))).scalar()
