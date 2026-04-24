from app.api.v1 import api_v1
from app.middleware.auth import internal_api_key_required
from app.services import booking_service
from app.utils.responses import success_response


@api_v1.route('/internal/expire-holds', methods=['POST'])
@internal_api_key_required
def expire_holds():
    count = booking_service.system_expire_holds()
    return success_response({'expired_count': count})
