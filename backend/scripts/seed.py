"""Seed script: creates admin user + sample hostel + 2 rooms."""
from __future__ import annotations
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('APP_ENV', 'development')


def main() -> None:
    from app import create_app
    from app.extensions import db
    from app.models.user import User
    from app.models.hostel import Hostel
    from app.models.room import Room
    from app.utils.password import hash_password

    app = create_app()
    with app.app_context():
        if not db.session.execute(
            db.select(User).where(User.email == 'admin@hostel.local')
        ).scalar_one_or_none():
            admin = User(
                full_name='Super Admin',
                email='admin@hostel.local',
                password_hash=hash_password('Admin1234!'),
                role='admin',
                is_active=True,
            )
            db.session.add(admin)
            db.session.flush()
            print('Created admin: admin@hostel.local / Admin1234!')
        else:
            admin = db.session.execute(
                db.select(User).where(User.email == 'admin@hostel.local')
            ).scalar_one()
            print('Admin already exists.')

        if not db.session.execute(
            db.select(Hostel).where(Hostel.name == 'Demo Hostel')
        ).scalar_one_or_none():
            hostel = Hostel(
                admin_user_id=admin.id,
                name='Demo Hostel',
                description='A sample hostel for testing.',
                city='Mumbai',
                address='1 Marine Drive, Mumbai',
                status='active',
            )
            db.session.add(hostel)
            db.session.flush()
            r1 = Room(hostel_id=hostel.id, room_number='101', room_type='Dormitory',
                      capacity=6, price_per_night=500, availability_status='available')
            r2 = Room(hostel_id=hostel.id, room_number='201', room_type='Private',
                      capacity=2, price_per_night=1500, availability_status='available')
            db.session.add_all([r1, r2])
            print(f'Created hostel "{hostel.name}" with 2 rooms.')
        else:
            print('Demo hostel already exists.')

        db.session.commit()
        print('Seed complete.')


if __name__ == '__main__':
    main()
