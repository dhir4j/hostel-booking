from flask import Blueprint
from app.utils.responses import success_response

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/healthz')
def healthz():
    return success_response({'status': 'ok'})


# Import route modules to register them
from app.api.v1 import auth, users, hostels, bookings, payments, internal  # noqa: F401, E402
from app.api.v1.admin import bp as admin_bp  # noqa: F401, E402
api_v1.register_blueprint(admin_bp)
