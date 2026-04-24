import logging
import traceback
from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from sqlalchemy.exc import IntegrityError
from app.utils.errors import AppError
from app.utils.responses import error_response

logger = logging.getLogger(__name__)


def init_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return error_response(e.code, e.message, e.details, status=e.status_code)

    @app.errorhandler(MarshmallowValidationError)
    def handle_validation_error(e):
        return error_response('VALIDATION_ERROR', 'Validation failed', details=e.messages, status=400)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        logger.warning('DB IntegrityError: %s', str(e.orig))
        return error_response('CONFLICT', 'Resource conflict or duplicate entry', status=409)

    @app.errorhandler(404)
    def handle_404(e):
        return error_response('NOT_FOUND', 'Resource not found', status=404)

    @app.errorhandler(405)
    def handle_405(e):
        return error_response('METHOD_NOT_ALLOWED', 'Method not allowed', status=405)

    @app.errorhandler(429)
    def handle_429(e):
        return error_response('RATE_LIMITED', 'Too many requests', status=429)

    @app.errorhandler(Exception)
    def handle_generic(e):
        logger.error('Unhandled exception: %s\n%s', str(e), traceback.format_exc())
        return error_response('INTERNAL_ERROR', 'An internal error occurred', status=500)
