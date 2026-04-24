from flask import request
from app.api.v1.admin import bp
from app.services import analytics_service
from app.utils.responses import success_response
from app.middleware.auth import role_required
from marshmallow import Schema, fields, validate

class AnalyticsQuerySchema(Schema):
    date_from = fields.Date(load_default=None)
    date_to = fields.Date(load_default=None)
    granularity = fields.Str(load_default='daily', validate=validate.OneOf(['daily', 'weekly', 'monthly']))

@bp.route('/analytics/summary', methods=['GET'])
@role_required('admin')
def analytics_summary():
    query = AnalyticsQuerySchema().load(request.args)
    result = analytics_service.summary(**query)
    return success_response({'analytics': result})
