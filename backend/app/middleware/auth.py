import functools
import hmac
from flask import request, g, current_app
from app.utils.tokens import decode_token
from app.utils.responses import error_response


def jwt_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error_response('UNAUTHORIZED', 'Missing or invalid authorization header', status=401)
        token = auth_header[7:]
        try:
            payload = decode_token(token, expected_type='access')
            g.current_user_id = int(payload['sub'])
            g.current_user_role = payload.get('role')
            g.jwt_jti = payload.get('jti')
        except Exception as e:
            return error_response('UNAUTHORIZED', str(e), status=401)
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(fn):
        @functools.wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            if g.get('current_user_role') not in roles:
                return error_response('FORBIDDEN', 'Insufficient permissions', status=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def optional_jwt(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        g.current_user_id = None
        g.current_user_role = None
        g.jwt_jti = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            try:
                payload = decode_token(token, expected_type='access')
                g.current_user_id = int(payload['sub'])
                g.current_user_role = payload.get('role')
                g.jwt_jti = payload.get('jti')
            except Exception:
                pass
        return fn(*args, **kwargs)
    return wrapper


def internal_api_key_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-Internal-API-Key', '')
        expected_key = current_app.config.get('INTERNAL_API_KEY', '')
        if not expected_key or not hmac.compare_digest(provided_key.encode(), expected_key.encode()):
            return error_response('UNAUTHORIZED', 'Invalid internal API key', status=401)
        return fn(*args, **kwargs)
    return wrapper
