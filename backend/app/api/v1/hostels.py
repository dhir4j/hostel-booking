import math

from flask import request
from app.api.v1 import api_v1
from app.services import hostel_service
from app.schemas.hostel import HostelListQuerySchema, HostelOutSchema, HostelSummarySchema
from app.utils.responses import success_response
from app.middleware.auth import optional_jwt


@api_v1.route('/hostels', methods=['GET'])
@optional_jwt
def list_hostels():
    query = HostelListQuerySchema().load(request.args)
    page = query.pop('page', 1)
    per_page = query.pop('per_page', 20)
    items, total = hostel_service.search_hostels(page=page, per_page=per_page, **query)
    meta = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': math.ceil(total / per_page) if per_page else 1,
    }
    return success_response({'items': HostelSummarySchema(many=True).dump(items)}, meta=meta)


@api_v1.route('/hostels/<int:hostel_id>', methods=['GET'])
@optional_jwt
def get_hostel(hostel_id):
    hostel = hostel_service.get_hostel(hostel_id)
    return success_response({'hostel': HostelOutSchema().dump(hostel)})
