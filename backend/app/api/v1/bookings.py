import math

from flask import request, g

from app.api.v1 import api_v1
from app.middleware.auth import jwt_required
from app.schemas.booking import BookingCreateSchema, BookingListQuerySchema, BookingOutSchema
from app.services import booking_service
from app.utils.responses import success_response


@api_v1.route('/bookings', methods=['POST'])
@jwt_required
def create_booking():
    data = BookingCreateSchema().load(request.get_json() or {})
    booking = booking_service.create_booking(user_id=g.current_user_id, **data)
    return success_response({'booking': BookingOutSchema().dump(booking)}, status=201)


@api_v1.route('/bookings/my', methods=['GET'])
@jwt_required
def list_my_bookings():
    query = BookingListQuerySchema().load(request.args)
    page = query.pop('page', 1)
    per_page = query.pop('per_page', 20)
    items, total = booking_service.list_my_bookings(
        g.current_user_id, page=page, per_page=per_page, **query
    )
    meta = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': math.ceil(total / per_page) if per_page else 1,
    }
    return success_response({'items': BookingOutSchema(many=True).dump(items)}, meta=meta)


@api_v1.route('/bookings/<int:booking_id>', methods=['GET'])
@jwt_required
def get_booking(booking_id):
    booking = booking_service.get_booking(booking_id, g.current_user_id, g.current_user_role)
    return success_response({'booking': BookingOutSchema().dump(booking)})


@api_v1.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@jwt_required
def cancel_booking(booking_id):
    booking = booking_service.cancel_booking(booking_id, g.current_user_id, g.current_user_role)
    return success_response({'booking': BookingOutSchema().dump(booking)})
