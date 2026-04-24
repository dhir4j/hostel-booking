from flask import request, g
from app.api.v1 import api_v1
from app.services import user_service, auth_service
from app.schemas.user import UserOutSchema, UserUpdateSchema
from app.schemas.auth import ChangePasswordSchema
from app.utils.responses import success_response
from app.middleware.auth import jwt_required


@api_v1.route('/users/me', methods=['GET'])
@jwt_required
def get_me():
    user = user_service.get_me(g.current_user_id)
    return success_response({'user': UserOutSchema().dump(user)})


@api_v1.route('/users/me', methods=['PATCH'])
@jwt_required
def update_me():
    data = UserUpdateSchema().load(request.get_json() or {})
    user = user_service.update_me(g.current_user_id, **data)
    return success_response({'user': UserOutSchema().dump(user)})


@api_v1.route('/users/me/change-password', methods=['POST'])
@jwt_required
def change_password():
    data = ChangePasswordSchema().load(request.get_json() or {})
    auth_service.change_password(g.current_user_id, data['current_password'], data['new_password'])
    return success_response({})
