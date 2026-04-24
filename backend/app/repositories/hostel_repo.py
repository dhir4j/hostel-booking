from sqlalchemy import select, func, exists
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models.hostel import Hostel, HostelImage, Amenity, hostel_amenities
from app.models.room import Room


def get_by_id(hostel_id: int) -> Hostel | None:
    stmt = (
        select(Hostel)
        .where(Hostel.id == hostel_id)
        .options(selectinload(Hostel.images), selectinload(Hostel.amenities))
    )
    return db.session.execute(stmt).scalar_one_or_none()


def list_public(
    city: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Hostel], int]:
    stmt = select(Hostel).where(Hostel.status == 'active')

    if city:
        stmt = stmt.where(Hostel.city.ilike(f'%{city}%'))

    if min_price is not None:
        price_subq = select(Room.hostel_id).where(
            Room.hostel_id == Hostel.id,
            Room.price_per_night >= min_price,
        )
        stmt = stmt.where(exists(price_subq))

    if max_price is not None:
        price_subq = select(Room.hostel_id).where(
            Room.hostel_id == Hostel.id,
            Room.price_per_night <= max_price,
        )
        stmt = stmt.where(exists(price_subq))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    rows = db.session.execute(stmt).scalars().all()
    return list(rows), total


def list_by_admin(
    admin_user_id: int,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    stmt = select(Hostel).where(Hostel.admin_user_id == admin_user_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    rows = db.session.execute(stmt).scalars().all()
    return list(rows), total


def create(admin_user_id: int, name: str, city: str, address: str, **kwargs) -> Hostel:
    hostel = Hostel(
        admin_user_id=admin_user_id,
        name=name,
        city=city,
        address=address,
        **kwargs,
    )
    db.session.add(hostel)
    db.session.flush()
    return hostel


def update(hostel: Hostel, **kwargs) -> Hostel:
    for k, v in kwargs.items():
        setattr(hostel, k, v)
    db.session.flush()
    return hostel


def soft_delete(hostel: Hostel) -> None:
    hostel.status = 'inactive'
    db.session.flush()


def add_image(hostel_id: int, image_url: str, is_primary: bool = False) -> HostelImage:
    image = HostelImage(hostel_id=hostel_id, image_url=image_url, is_primary=is_primary)
    db.session.add(image)
    db.session.flush()
    return image


def delete_image(image_id: int) -> None:
    image = db.session.get(HostelImage, image_id)
    if image:
        db.session.delete(image)
        db.session.flush()


def get_amenity_by_id(amenity_id: int) -> Amenity | None:
    return db.session.get(Amenity, amenity_id)


def list_amenities() -> list[Amenity]:
    stmt = select(Amenity)
    return list(db.session.execute(stmt).scalars().all())
