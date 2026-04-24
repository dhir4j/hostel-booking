import math
from flask import request, g
from app.api.v1.admin import bp
from app.services import booking_service
from app.schemas.booking import BookingOutSchema, BookingActionSchema, AdminBookingListQuerySchema
from app.utils.responses import success_response
from app.middleware.auth import role_required

@bp.route('/bookings', methods=['GET'])
@role_required('admin')
def list_bookings():
    query = AdminBookingListQuerySchema().load(request.args)
    page = query.pop('page', 1)
    per_page = query.pop('per_page', 20)
    from app.repositories import booking_repo
    items, total = booking_repo.list_admin(page=page, per_page=per_page, **query)
    meta = {'page': page, 'per_page': per_page, 'total': total,
            'total_pages': math.ceil(total / per_page) if per_page else 1}
    return success_response({'items': BookingOutSchema(many=True).dump(items)}, meta=meta)

@bp.route('/bookings/<int:booking_id>', methods=['GET'])
@role_required('admin')
def get_booking(booking_id):
    booking = booking_service.get_booking(booking_id, g.current_user_id, 'admin')
    return success_response({'booking': BookingOutSchema().dump(booking)})

@bp.route('/bookings/<int:booking_id>/approve', methods=['POST'])
@role_required('admin')
def approve_booking(booking_id):
    data = BookingActionSchema().load(request.get_json() or {})
    booking = booking_service.admin_approve(booking_id, g.current_user_id, notes=data.get('admin_notes'))
    return success_response({'booking': BookingOutSchema().dump(booking)})

@bp.route('/bookings/<int:booking_id>/reject', methods=['POST'])
@role_required('admin')
def reject_booking(booking_id):
    data = BookingActionSchema().load(request.get_json() or {})
    booking = booking_service.admin_reject(booking_id, g.current_user_id, notes=data.get('admin_notes'))
    return success_response({'booking': BookingOutSchema().dump(booking)})

@bp.route('/bookings/<int:booking_id>/checkin', methods=['POST'])
@role_required('admin')
def checkin_booking(booking_id):
    booking = booking_service.admin_checkin(booking_id, g.current_user_id)
    return success_response({'booking': BookingOutSchema().dump(booking)})

@bp.route('/bookings/<int:booking_id>/checkout', methods=['POST'])
@role_required('admin')
def checkout_booking(booking_id):
    booking = booking_service.admin_checkout(booking_id, g.current_user_id)
    return success_response({'booking': BookingOutSchema().dump(booking)})

@bp.route('/bookings/<int:booking_id>/complete', methods=['POST'])
@role_required('admin')
def complete_booking(booking_id):
    booking = booking_service.admin_complete(booking_id, g.current_user_id)
    return success_response({'booking': BookingOutSchema().dump(booking)})
