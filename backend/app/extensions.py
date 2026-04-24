"""Module-level singletons for Flask extensions.

These are instantiated here with no-op defaults so sub-modules can import them
freely. The app factory (:func:`app.create_app`) is responsible for all
``init_app`` / configuration wiring.
"""

from __future__ import annotations

from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Database session + ORM metadata. Models import ``db`` to inherit from
# ``db.Model``.
db = SQLAlchemy()

# Alembic integration. ``migrate.init_app(app, db)`` is called in the factory.
migrate = Migrate()

# Rate limiter. We pass an empty ``default_limits`` list and set the real
# storage_uri from config inside ``init_app`` — passing ``storage_uri`` here
# would snapshot ``os.environ`` at import time and ignore later config.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    headers_enabled=True,
)

# SMTP mailer. Sends are best-effort; callers must not fail the request on
# mail errors.
mail = Mail()

# CORS. The factory calls ``cors.init_app(app, resources=..., supports_credentials=True)``
# with the exact origin list.
cors = CORS()


__all__ = ["db", "migrate", "limiter", "mail", "cors"]
