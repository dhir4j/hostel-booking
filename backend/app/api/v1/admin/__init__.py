from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.api.v1.admin import hostels, bookings, payments, analytics  # noqa: F401, E402
