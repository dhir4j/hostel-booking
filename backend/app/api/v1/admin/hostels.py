import math
from flask import request, g
from app.api.v1.admin import bp
from app.services import hostel_service, room_service
from app.schemas.hostel import HostelCreateSchema, HostelUpdateSchema, HostelOutSchema, HostelImageSchema
from app.schemas.room import RoomCreateSchema, RoomUpdateSchema, RoomOutSchema, RoomBlockCreateSchema, RoomBlockOutSchema
from app.utils.responses import success_response
from app.middleware.auth import role_required

# --- Hostels ---

@bp.route('/hostels', methods=['GET'])
@role_required('admin')
def list_hostels():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    items, total = hostel_service.admin_list_hostels(g.current_user_id, page=page, per_page=per_page)
    meta = {'page': page, 'per_page': per_page, 'total': total,
            'total_pages': math.ceil(total / per_page) if per_page else 1}
    return success_response({'items': HostelOutSchema(many=True).dump(items)}, meta=meta)

@bp.route('/hostels', methods=['POST'])
@role_required('admin')
def create_hostel():
    data = HostelCreateSchema().load(request.get_json() or {})
    hostel = hostel_service.admin_create_hostel(admin_user_id=g.current_user_id, **data)
    return success_response({'hostel': HostelOutSchema().dump(hostel)}, status=201)

@bp.route('/hostels/<int:hostel_id>', methods=['GET'])
@role_required('admin')
def get_hostel(hostel_id):
    hostel = hostel_service.get_hostel(hostel_id, admin=True)
    return success_response({'hostel': HostelOutSchema().dump(hostel)})

@bp.route('/hostels/<int:hostel_id>', methods=['PATCH'])
@role_required('admin')
def update_hostel(hostel_id):
    data = HostelUpdateSchema().load(request.get_json() or {})
    hostel = hostel_service.admin_update_hostel(hostel_id, actor_user_id=g.current_user_id, **data)
    return success_response({'hostel': HostelOutSchema().dump(hostel)})

@bp.route('/hostels/<int:hostel_id>', methods=['DELETE'])
@role_required('admin')
def delete_hostel(hostel_id):
    hostel_service.admin_soft_delete_hostel(hostel_id, actor_user_id=g.current_user_id)
    return success_response({})

@bp.route('/hostels/<int:hostel_id>/images', methods=['POST'])
@role_required('admin')
def add_image(hostel_id):
    data = request.get_json() or {}
    image = hostel_service.add_image(hostel_id, data.get('image_url', ''), data.get('is_primary', False), g.current_user_id)
    return success_response({'image': HostelImageSchema().dump(image)}, status=201)

@bp.route('/hostels/<int:hostel_id>/images/<int:image_id>', methods=['DELETE'])
@role_required('admin')
def delete_image(hostel_id, image_id):
    hostel_service.delete_image(image_id, actor_user_id=g.current_user_id)
    return success_response({})

# --- Rooms ---

@bp.route('/rooms', methods=['GET'])
@role_required('admin')
def list_rooms():
    hostel_id = request.args.get('hostel_id', type=int)
    items = room_service.list_rooms(hostel_id) if hostel_id else []
    return success_response({'items': RoomOutSchema(many=True).dump(items)})

@bp.route('/rooms', methods=['POST'])
@role_required('admin')
def create_room():
    data = RoomCreateSchema().load(request.get_json() or {})
    room = room_service.admin_create_room(actor_user_id=g.current_user_id, **data)
    return success_response({'room': RoomOutSchema().dump(room)}, status=201)

@bp.route('/rooms/<int:room_id>', methods=['GET'])
@role_required('admin')
def get_room(room_id):
    room = room_service.get_room(room_id)
    return success_response({'room': RoomOutSchema().dump(room)})

@bp.route('/rooms/<int:room_id>', methods=['PATCH'])
@role_required('admin')
def update_room(room_id):
    data = RoomUpdateSchema().load(request.get_json() or {})
    room = room_service.admin_update_room(room_id, actor_user_id=g.current_user_id, **data)
    return success_response({'room': RoomOutSchema().dump(room)})

@bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@role_required('admin')
def delete_room(room_id):
    room_service.admin_soft_delete_room(room_id, actor_user_id=g.current_user_id)
    return success_response({})

# --- Availability Blocks ---

@bp.route('/availability/blocks', methods=['GET'])
@role_required('admin')
def list_blocks():
    room_id = request.args.get('room_id', type=int)
    items = room_service.list_blocks(room_id) if room_id else []
    return success_response({'items': RoomBlockOutSchema(many=True).dump(items)})

@bp.route('/availability/blocks', methods=['POST'])
@role_required('admin')
def create_block():
    data = RoomBlockCreateSchema().load(request.get_json() or {})
    block = room_service.admin_create_block(actor_user_id=g.current_user_id, **data)
    return success_response({'block': RoomBlockOutSchema().dump(block)}, status=201)

@bp.route('/availability/blocks/<int:block_id>', methods=['DELETE'])
@role_required('admin')
def delete_block(block_id):
    room_service.admin_delete_block(block_id, actor_user_id=g.current_user_id)
    return success_response({})
