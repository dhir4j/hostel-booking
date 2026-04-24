import math
from flask import request, g
from app.api.v1.admin import bp
from app.services import payment_service
from app.schemas.payment import PaymentOutSchema, AdminPaymentListQuerySchema
from app.utils.responses import success_response
from app.middleware.auth import role_required

@bp.route('/payments', methods=['GET'])
@role_required('admin')
def list_payments():
    query = AdminPaymentListQuerySchema().load(request.args)
    page = query.pop('page', 1)
    per_page = query.pop('per_page', 20)
    from app.repositories import payment_repo
    items, total = payment_repo.list_admin(page=page, per_page=per_page, **query)
    meta = {'page': page, 'per_page': per_page, 'total': total,
            'total_pages': math.ceil(total / per_page) if per_page else 1}
    return success_response({'items': PaymentOutSchema(many=True).dump(items)}, meta=meta)

@bp.route('/payments/<int:payment_id>', methods=['GET'])
@role_required('admin')
def get_payment(payment_id):
    from app.repositories import payment_repo
    from app.utils.errors import NotFoundError
    p = payment_repo.get_by_id(payment_id)
    if not p:
        raise NotFoundError('Payment not found')
    return success_response({'payment': PaymentOutSchema().dump(p)})

@bp.route('/payments/<int:payment_id>/reconcile', methods=['POST'])
@role_required('admin')
def reconcile_payment(payment_id):
    result = payment_service.admin_reconcile(payment_id, g.current_user_id)
    return success_response({'payment': PaymentOutSchema().dump(result)})

@bp.route('/payments/<int:payment_id>/refund', methods=['POST'])
@role_required('admin')
def refund_payment(payment_id):
    result = payment_service.admin_refund(payment_id, g.current_user_id)
    return success_response({'payment': PaymentOutSchema().dump(result)})
