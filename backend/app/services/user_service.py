"""User profile service."""

from __future__ import annotations

from app.repositories import user_repo
from app.extensions import db
from app.utils.errors import NotFoundError


def get_me(user_id: int):
    """Fetch the current user by id.

    Raises:
        NotFoundError: If no user with that id exists.
    """
    user = user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


def update_me(
    user_id: int,
    full_name: str | None = None,
    phone: str | None = None,
):
    """Update mutable profile fields for the current user.

    Only non-None arguments are applied.

    Raises:
        NotFoundError: If no user with that id exists.
    """
    user = user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("User not found")

    updates = {}
    if full_name is not None:
        updates["full_name"] = full_name
    if phone is not None:
        updates["phone"] = phone

    if updates:
        user_repo.update(user, **updates)
        db.session.commit()

    return user
