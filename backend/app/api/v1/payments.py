from flask import request, g

from app.api.v1 import api_v1
from app.middleware.auth import jwt_required
from app.schemas.payment import PaymentIntentRequestSchema
from app.services import payment_service
from app.utils.errors import PaymentError
from app.utils.responses import error_response, success_response


@api_v1.route('/payments/create-intent', methods=['POST'])
@jwt_required
def create_intent():
    data = PaymentIntentRequestSchema().load(request.get_json() or {})
    result = payment_service.create_intent(data['booking_id'], g.current_user_id)
    return success_response({'payment': result}, status=201)


@api_v1.route('/payments/webhook/<provider>', methods=['POST'])
def payment_webhook(provider):
    # Raw bytes must be read before any JSON parsing touches the body.
    raw_body = request.get_data(cache=True, as_text=False)
    headers = request.headers
    try:
        result = payment_service.handle_webhook(provider, headers, raw_body)
    except PaymentError as e:
        return error_response(e.code, e.message, status=400)
    except Exception as e:
        return error_response('WEBHOOK_ERROR', str(e), status=400)
    return success_response({'received': True})


@api_v1.route('/payments/<int:booking_id>/status', methods=['GET'])
@jwt_required
def payment_status(booking_id):
    result = payment_service.get_status(booking_id, g.current_user_id, g.current_user_role)
    return success_response({'status': result})
