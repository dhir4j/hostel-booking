import uuid
import logging
from flask import g, request


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        from flask import has_request_context
        record.request_id = g.get('request_id', '-') if has_request_context() else '-'
        return True


def init_request_id(app):
    @app.before_request
    def set_request_id():
        request_id = request.headers.get('X-Request-ID') or uuid.uuid4().hex
        g.request_id = request_id

    @app.after_request
    def echo_request_id(response):
        response.headers['X-Request-ID'] = g.get('request_id', '-')
        return response

    # Install filter on root logger
    f = RequestIDFilter()
    logging.getLogger().addFilter(f)
