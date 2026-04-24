"""Hostel management service."""

from __future__ import annotations

from app.repositories import hostel_repo, audit_repo
from app.extensions import db
from app.utils.errors import NotFoundError


def search_hostels(
    city: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    check_in=None,
    check_out=None,
    guests: int | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    """Return a paginated public hostel listing.

    Returns:
        (items, total)
    """
    return hostel_repo.list_public(
        city=city,
        min_price=min_price,
        max_price=max_price,
        page=page,
        per_page=per_page,
    )


def get_hostel(hostel_id: int, admin: bool = False):
    """Fetch a single hostel by id.

    Raises:
        NotFoundError: If not found, or if inactive and admin is False.
    """
    hostel = hostel_repo.get_by_id(hostel_id)
    if hostel is None:
        raise NotFoundError("Hostel not found")
    if not admin and hostel.status != "active":
        raise NotFoundError("Hostel not found")
    return hostel


def admin_list_hostels(
    admin_user_id: int,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    """Return hostels owned by the given admin user.

    Returns:
        (items, total)
    """
    return hostel_repo.list_by_admin(
        admin_user_id=admin_user_id,
        page=page,
        per_page=per_page,
    )


def admin_create_hostel(
    admin_user_id: int,
    name: str,
    city: str,
    address: str,
    **kwargs,
):
    """Create a new hostel, optionally assigning amenities.

    amenity_ids (list[int]) may be passed in kwargs and is handled separately.
    """
    amenity_ids: list[int] = kwargs.pop("amenity_ids", None) or []

    hostel = hostel_repo.create(
        admin_user_id=admin_user_id,
        name=name,
        city=city,
        address=address,
        **kwargs,
    )

    if amenity_ids:
        amenities = [
            hostel_repo.get_amenity_by_id(aid)
            for aid in amenity_ids
        ]
        hostel.amenities = [a for a in amenities if a is not None]
        db.session.flush()

    audit_repo.log(
        entity_type="hostel",
        entity_id=hostel.id,
        action="create",
        actor_user_id=admin_user_id,
    )
    db.session.commit()
    return hostel


def admin_update_hostel(hostel_id: int, actor_user_id: int, **kwargs):
    """Update hostel fields, optionally replacing amenities.

    amenity_ids (list[int]) may be passed in kwargs.

    Raises:
        NotFoundError: If hostel not found.
    """
    amenity_ids: list[int] | None = kwargs.pop("amenity_ids", None)

    hostel = hostel_repo.get_by_id(hostel_id)
    if hostel is None:
        raise NotFoundError("Hostel not found")

    if kwargs:
        hostel_repo.update(hostel, **kwargs)

    if amenity_ids is not None:
        amenities = [
            hostel_repo.get_amenity_by_id(aid)
            for aid in amenity_ids
        ]
        hostel.amenities = [a for a in amenities if a is not None]
        db.session.flush()

    audit_repo.log(
        entity_type="hostel",
        entity_id=hostel.id,
        action="update",
        actor_user_id=actor_user_id,
    )
    db.session.commit()
    return hostel


def admin_soft_delete_hostel(hostel_id: int, actor_user_id: int) -> None:
    """Mark a hostel as inactive.

    Raises:
        NotFoundError: If hostel not found.
    """
    hostel = hostel_repo.get_by_id(hostel_id)
    if hostel is None:
        raise NotFoundError("Hostel not found")

    hostel_repo.soft_delete(hostel)
    audit_repo.log(
        entity_type="hostel",
        entity_id=hostel_id,
        action="soft_delete",
        actor_user_id=actor_user_id,
    )
    db.session.commit()


def add_image(
    hostel_id: int,
    image_url: str,
    is_primary: bool = False,
    actor_user_id: int | None = None,
):
    """Add an image to a hostel.

    Raises:
        NotFoundError: If hostel not found.
    """
    hostel = hostel_repo.get_by_id(hostel_id)
    if hostel is None:
        raise NotFoundError("Hostel not found")

    image = hostel_repo.add_image(hostel_id, image_url, is_primary=is_primary)
    db.session.commit()
    return image


def delete_image(image_id: int, actor_user_id: int | None = None) -> None:
    """Delete a hostel image by id."""
    hostel_repo.delete_image(image_id)
    db.session.commit()
