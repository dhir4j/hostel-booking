"""Room management service."""

from __future__ import annotations

from app.repositories import room_repo, booking_repo, audit_repo
from app.extensions import db
from app.utils.errors import NotFoundError, ConflictError


def get_room(room_id: int):
    """Fetch a single room by id.

    Raises:
        NotFoundError: If not found.
    """
    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Room not found")
    return room


def list_rooms(hostel_id: int) -> list:
    """Return all rooms for a hostel."""
    return room_repo.list_by_hostel(hostel_id)


def admin_create_room(
    hostel_id: int,
    room_number: str,
    capacity: int,
    price_per_night: float,
    actor_user_id: int,
    **kwargs,
):
    """Create a room for the given hostel.

    Returns:
        The newly created Room instance.
    """
    room = room_repo.create(
        hostel_id=hostel_id,
        room_number=room_number,
        capacity=capacity,
        price_per_night=price_per_night,
        **kwargs,
    )
    audit_repo.log(
        entity_type="room",
        entity_id=room.id,
        action="create",
        actor_user_id=actor_user_id,
    )
    db.session.commit()
    return room


def admin_update_room(room_id: int, actor_user_id: int, **kwargs):
    """Update room fields.

    Raises:
        NotFoundError: If room not found.
    """
    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Room not found")

    room_repo.update(room, **kwargs)
    audit_repo.log(
        entity_type="room",
        entity_id=room_id,
        action="update",
        actor_user_id=actor_user_id,
    )
    db.session.commit()
    return room


def admin_soft_delete_room(room_id: int, actor_user_id: int) -> None:
    """Mark a room as unavailable.

    Raises:
        NotFoundError: If room not found.
    """
    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Room not found")

    room_repo.soft_delete(room)
    audit_repo.log(
        entity_type="room",
        entity_id=room_id,
        action="soft_delete",
        actor_user_id=actor_user_id,
    )
    db.session.commit()


def admin_create_block(
    room_id: int,
    start_date,
    end_date,
    reason: str,
    actor_user_id: int,
):
    """Block a room for a date range.

    Raises:
        NotFoundError: If room not found.
        ConflictError: If there are active bookings overlapping the block dates.
    """
    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Room not found")

    overlapping = booking_repo.find_overlapping(room_id, start_date, end_date)
    if overlapping:
        raise ConflictError(
            f"Cannot block room: {len(overlapping)} active booking(s) overlap the requested dates."
        )

    block = room_repo.create_block(room_id, start_date, end_date, reason)
    audit_repo.log(
        entity_type="room_block",
        entity_id=block.id,
        action="create",
        actor_user_id=actor_user_id,
    )
    db.session.commit()
    return block


def admin_delete_block(block_id: int, actor_user_id: int) -> None:
    """Delete a room block.

    Raises:
        NotFoundError: If the block does not exist.
    """
    deleted = room_repo.delete_block(block_id)
    if not deleted:
        raise NotFoundError("Room block not found")

    audit_repo.log(
        entity_type="room_block",
        entity_id=block_id,
        action="delete",
        actor_user_id=actor_user_id,
    )
    db.session.commit()


def list_blocks(room_id: int, from_date=None, to_date=None) -> list:
    """Return blocks for a room, optionally filtered by date range."""
    return room_repo.list_blocks(room_id, from_date=from_date, to_date=to_date)
