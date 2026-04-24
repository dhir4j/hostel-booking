from flask import request, make_response, current_app
from app.api.v1 import api_v1
from app.services import auth_service
from app.schemas.auth import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema, ChangePasswordSchema
from app.schemas.user import UserOutSchema
from app.utils.responses import success_response, error_response
from app.middleware.auth import jwt_required

REFRESH_COOKIE = 'refresh_token'


@api_v1.route('/auth/register', methods=['POST'])
def register():
    data = RegisterSchema().load(request.get_json() or {})
    user = auth_service.register_user(**data)
    return success_response({'user': UserOutSchema().dump(user)}, status=201)


@api_v1.route('/auth/login', methods=['POST'])
def login():
    data = LoginSchema().load(request.get_json() or {})
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    access_token, refresh_raw, user = auth_service.login(
        email=data['email'], password=data['password'],
        user_agent=user_agent, ip=ip
    )
    resp = make_response(success_response({'access_token': access_token, 'user': UserOutSchema().dump(user)}))
    _set_refresh_cookie(resp, refresh_raw)
    return resp


@api_v1.route('/auth/refresh', methods=['POST'])
def refresh():
    refresh_raw = request.cookies.get(REFRESH_COOKIE)
    if not refresh_raw:
        return error_response('UNAUTHORIZED', 'No refresh token', status=401)
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    access_token, new_refresh_raw = auth_service.refresh(refresh_raw, user_agent, ip)
    resp = make_response(success_response({'access_token': access_token}))
    _set_refresh_cookie(resp, new_refresh_raw)
    return resp


@api_v1.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():
    refresh_raw = request.cookies.get(REFRESH_COOKIE, '')
    auth_service.logout(refresh_raw)
    resp = make_response(success_response({}))
    resp.delete_cookie(REFRESH_COOKIE, path='/api/v1/auth')
    return resp


@api_v1.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = ForgotPasswordSchema().load(request.get_json() or {})
    auth_service.forgot_password(data['email'])
    return success_response({})


@api_v1.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = ResetPasswordSchema().load(request.get_json() or {})
    auth_service.reset_password(data['token'], data['new_password'])
    return success_response({})


def _set_refresh_cookie(resp, token: str):
    secure = not current_app.debug
    resp.set_cookie(
        REFRESH_COOKIE, token,
        httponly=True, secure=secure, samesite='Lax',
        path='/api/v1/auth',
        max_age=60 * 60 * 24 * int(current_app.config.get('JWT_REFRESH_TTL_DAYS', 7)),
    )
