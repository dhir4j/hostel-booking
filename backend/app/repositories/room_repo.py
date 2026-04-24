from sqlalchemy import select

from app.extensions import db
from app.models.room import Room, RoomBlock


def get_by_id(room_id: int) -> Room | None:
    return db.session.get(Room, room_id)


def list_by_hostel(hostel_id: int) -> list[Room]:
    stmt = select(Room).where(Room.hostel_id == hostel_id)
    return list(db.session.execute(stmt).scalars().all())


def create(**kwargs) -> Room:
    room = Room(**kwargs)
    db.session.add(room)
    db.session.flush()
    return room


def update(room: Room, **kwargs) -> Room:
    for k, v in kwargs.items():
        setattr(room, k, v)
    db.session.flush()
    return room


def soft_delete(room: Room) -> None:
    room.availability_status = 'unavailable'
    db.session.flush()


def find_available_locked(room_id: int, check_in, check_out) -> Room | None:
    stmt = (
        select(Room)
        .where(
            Room.id == room_id,
            Room.availability_status == 'available',
        )
        .with_for_update(of=Room)
    )
    return db.session.execute(stmt).scalar_one_or_none()


def list_blocks(room_id: int, from_date=None, to_date=None) -> list[RoomBlock]:
    stmt = select(RoomBlock).where(RoomBlock.room_id == room_id)
    if from_date is not None:
        stmt = stmt.where(RoomBlock.end_date > from_date)
    if to_date is not None:
        stmt = stmt.where(RoomBlock.start_date < to_date)
    return list(db.session.execute(stmt).scalars().all())


def create_block(room_id: int, start_date, end_date, reason: str) -> RoomBlock:
    block = RoomBlock(room_id=room_id, start_date=start_date, end_date=end_date, reason=reason)
    db.session.add(block)
    db.session.flush()
    return block


def delete_block(block_id: int) -> bool:
    block = db.session.get(RoomBlock, block_id)
    if block is None:
        return False
    db.session.delete(block)
    db.session.flush()
    return True
