import logging
import os
from flask import Flask
from dotenv import load_dotenv


def create_app(config_name=None):
    load_dotenv()

    app = Flask(__name__)

    # Load config
    from app.config import get_config
    cfg = get_config(config_name)
    app.config.from_object(cfg)

    # Init extensions
    from app.extensions import db, migrate, limiter, mail, cors
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', [])}},
        supports_credentials=True,
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    )
    mail.init_app(app)

    # Middleware
    from app.middleware.request_id import init_request_id
    from app.middleware.security_headers import init_security_headers
    from app.middleware.error_handlers import init_error_handlers
    init_request_id(app)
    init_security_headers(app)
    init_error_handlers(app)

    # Register blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Import models so Alembic autogenerates them
    from app import models  # noqa: F401

    # Configure logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(request_id)s] %(name)s %(levelname)s %(message)s',
    )

    return app
