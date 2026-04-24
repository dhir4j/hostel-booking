# Flask Backend Implementation Plan — Hostel Management API

**Target path:** `/home/dhir4j/Documents/Dhillon/hostel-application/backend/`
**Spec source:** `.omc/autopilot/spec.md`
**Stack:** Python 3.11+, Flask, SQLAlchemy, Flask-Migrate, PostgreSQL, PyJWT, bcrypt, Marshmallow, Flask-Limiter, Flask-CORS, pytest.

---

## Global Conventions (apply to every wave)

- All files use absolute imports rooted at `app.*`.
- All responses pass through `app/utils/responses.py` helpers (`success_response`, `error_response`). No raw `jsonify` at route level — keeps envelope consistent (`{success, data, error, meta}`).
- Datetimes are timezone-aware UTC (`datetime.now(timezone.utc)`). Never `datetime.utcnow()` (naive, deprecated in 3.12).
- Decimal/money fields use `decimal.Decimal`, never float. Marshmallow serializes with `as_string=True`.
- Money math happens in services, not routes and not models.
- All DB writes flow through a repository function that accepts `db.session` implicitly; services manage commit/rollback boundaries. Routes never call `db.session.commit()`.
- Logger name mirrors module path (`logging.getLogger(__name__)`). Request ID is injected via `middleware/request_id.py` and must be included in every log line (use `logging.Filter`).
- Every public endpoint has at least one test; every state-transition branch has one test.
- Every enum is mirrored as a Python `enum.Enum` in `app/models/<entity>.py` and referenced from services/schemas — never hardcode strings.

---

## Wave 1 — Foundation (SEQUENTIAL, single agent)

**Why sequential:** later waves import from these modules. A misconfigured `create_app` or `extensions` poisons everything downstream.

### 1.1 Root scaffolding

**Files to create:**
- `backend/requirements.txt`
- `backend/requirements-dev.txt`
- `backend/.env.example`
- `backend/.flaskenv`
- `backend/Makefile`
- `backend/pytest.ini`
- `backend/wsgi.py`
- `backend/.gitignore`
- `backend/README.md` (brief)

**Key implementation notes:**
- `requirements.txt` pins: `Flask==3.0.*`, `Flask-SQLAlchemy==3.1.*`, `Flask-Migrate==4.0.*`, `Flask-Limiter==3.5.*`, `Flask-CORS==4.0.*`, `Flask-Mail==0.10.*`, `SQLAlchemy==2.0.*`, `psycopg2-binary==2.9.*` (fallback to `psycopg[binary]==3.2.*` if PythonAnywhere allows), `alembic==1.13.*`, `PyJWT==2.8.*`, `bcrypt==4.1.*` (direct — passlib is unmaintained on 3.12+, but spec says passlib; use `passlib[bcrypt]==1.7.4` with `bcrypt<4.1` pinned to avoid the known `__about__` attribute error), `marshmallow==3.21.*`, `python-dotenv==1.0.*`, `gunicorn==21.2.*`.
- `requirements-dev.txt` pins: `pytest==8.*`, `pytest-flask==1.3.*`, `pytest-cov==5.*`, `freezegun==1.5.*`, `factory-boy==3.3.*`, `faker==25.*`, `responses==0.25.*` (for stripe/razorpay stubs).
- `.flaskenv`: `FLASK_APP=wsgi:app`, `FLASK_DEBUG=1`.
- `.env.example`: all vars from spec §7, each with safe placeholder (no real secrets); include clear comments per var.
- `pytest.ini`: `[pytest]` with `testpaths=tests`, `addopts=-ra --strict-markers --cov=app --cov-report=term-missing`, `markers=unit api integration slow`.
- `Makefile` targets: `install`, `install-dev`, `run`, `test`, `test-cov`, `migrate`, `upgrade`, `downgrade`, `seed`, `lint`, `fmt`. Use tabs for recipe indentation.
- `wsgi.py`: `from app import create_app; app = create_app()`. Nothing else. PythonAnywhere reads this.

**Gotcha:** PythonAnywhere's free-tier Python build of `psycopg2` has historically been fragile. Prefer `psycopg2-binary`. Keep `psycopg[binary]==3.2.*` as an alternate pin commented in requirements for a later migration.

### 1.2 Config system

**Files to create:**
- `backend/app/__init__.py` (stub only — real factory in 1.4)
- `backend/app/config/__init__.py` (re-exports `get_config(env_name)`)
- `backend/app/config/base.py`
- `backend/app/config/development.py`
- `backend/app/config/testing.py`
- `backend/app/config/production.py`

**Key implementation notes:**
- `base.py` defines `BaseConfig` with every env var from spec §7 resolved via `os.environ.get` with safe defaults for non-secrets and `None` for secrets.
- `base.py` enforces `SECRET_KEY` and `JWT_SECRET_KEY` in `__init_subclass__` or via a `validate()` classmethod called at app init — production must raise if missing.
- `development.py`: `DEBUG=True`, `SQLALCHEMY_ECHO=False` (too noisy; toggle via env), permissive CORS.
- `testing.py`: `TESTING=True`, `WTF_CSRF_ENABLED=False`, `JWT_ACCESS_TTL_MINUTES=5`, `HOLD_TTL_MINUTES=1`, `RATELIMIT_ENABLED=False`, `SQLALCHEMY_DATABASE_URI` sourced from `TEST_DATABASE_URL`.
- `production.py`: strict validation, forces HTTPS cookies, adds `PROPAGATE_EXCEPTIONS=True` so error handlers run.
- `get_config(env_name: str) -> type[BaseConfig]` picks class from `APP_ENV`; default `development`.

**Gotcha:** `SQLALCHEMY_DATABASE_URI` coming from `DATABASE_URL` must be rewritten if it starts with `postgres://` (Heroku-style) to `postgresql://` — SQLAlchemy 2.x rejects the legacy scheme. Do it in `base.py`.

### 1.3 Extensions

**Files to create:**
- `backend/app/extensions.py`

**Key implementation notes:**
- Define module-level singletons: `db = SQLAlchemy()`, `migrate = Migrate()`, `limiter = Limiter(key_func=get_remote_address, storage_uri=<lazy>, default_limits=[])`, `mail = Mail()`, `cors = CORS()`.
- Do NOT call `init_app` here. Only in factory.
- `Limiter` must be instantiated with a no-op default, and its `storage_uri` is set from config inside `init_app` — instantiating with a stale URI causes `RATELIMIT_STORAGE_URI=memory://` to be ignored.

### 1.4 App factory

**Files to create:**
- `backend/app/__init__.py` (final version)

**Key implementation notes:**
- `create_app(config_name: str | None = None) -> Flask`.
- Load `.env` explicitly at the top (`python-dotenv`) in case running outside Flask CLI.
- Order in factory:
  1. Build `Flask(__name__)`, load config class.
  2. Init extensions: `db`, `migrate.init_app(app, db)`, `limiter`, `cors.init_app(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}}, supports_credentials=True)`, `mail`.
  3. Register request ID middleware (before anything else).
  4. Register security headers middleware.
  5. Register blueprints: `app.api.v1` under `/api/v1`.
  6. Register error handlers.
  7. Configure logging (structured; JSON in prod, plain in dev).
  8. Register CLI commands (seed, expire-holds).
- Import models inside factory (`from app import models  # noqa: F401`) so Alembic autogenerate sees them.
- Do NOT eagerly import services at factory time (they import repos which import models — fine), but avoid circular imports by never having routes import the factory.

**Gotcha:** `supports_credentials=True` on CORS plus a refresh-token cookie means the frontend MUST send explicit `Origin` — and the backend must NOT set `Access-Control-Allow-Origin: *`. Ensure `CORS_ORIGINS` is a list, not `"*"`, when credentials=True.

### 1.5 Utility modules

**Files to create:**
- `backend/app/utils/__init__.py`
- `backend/app/utils/responses.py`
- `backend/app/utils/pagination.py`
- `backend/app/utils/password.py`
- `backend/app/utils/tokens.py`
- `backend/app/utils/dates.py`
- `backend/app/utils/errors.py` (custom exception hierarchy)

**Key implementation notes:**
- `responses.py`:
  - `success_response(data=None, meta=None, status=200) -> tuple[Response, int]`
  - `error_response(code: str, message: str, details=None, status=400) -> tuple[Response, int]`
  - Error codes are UPPER_SNAKE, defined as constants in `utils/errors.py`: `INVALID_CREDENTIALS`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`, `INVALID_STATE_TRANSITION`, `CONFLICT`, `ROOM_UNAVAILABLE`, `HOLD_EXPIRED`, `PAYMENT_FAILED`, `RATE_LIMITED`, `INTERNAL_ERROR`.
- `pagination.py`:
  - `paginate(query, page: int, per_page: int, max_per_page: int = 100)` returns `(items, meta)` with `{page, per_page, total, total_pages, has_next, has_prev}`.
  - Clamp `per_page` to `max_per_page`.
- `password.py`: `hash_password(plain) -> str`, `verify_password(plain, hashed) -> bool`. Use `passlib.hash.bcrypt.using(rounds=12)` per spec.
- `tokens.py`:
  - `encode_access_token(user_id, role, jti=None)` — 15 min, `type=access`.
  - `encode_refresh_token(user_id, jti=None)` — 7 days, `type=refresh`.
  - `decode_token(token, expected_type)` — raises `InvalidTokenError`, `ExpiredSignatureError`.
  - `generate_reset_token()` — returns `(raw, sha256_hex)`. Store only the hash.
  - `hash_token(raw)` — used for refresh-token hashing before DB write.
  - JWT `sub` claim MUST be a string per RFC 7519 + PyJWT 2.10+ (it validates). Cast `user_id` to `str`.
- `dates.py`:
  - `parse_iso_date(s) -> date` with clear error.
  - `validate_booking_dates(check_in, check_out)` — both future-or-today, check_out > check_in, max span e.g. 90 days.
  - `ranges_overlap(a_start, a_end, b_start, b_end) -> bool` — pure function, half-open intervals `[start, end)`.

**Gotcha:** `passlib` + `bcrypt>=4.1` raises `AttributeError: module 'bcrypt' has no attribute '__about__'`. Pin `bcrypt<4.1` in requirements.txt. This will bite in CI if unpinned.

### 1.6 Middleware

**Files to create:**
- `backend/app/middleware/__init__.py`
- `backend/app/middleware/auth.py` — `jwt_required`, `role_required('admin')`, `optional_jwt`
- `backend/app/middleware/error_handlers.py`
- `backend/app/middleware/request_id.py`
- `backend/app/middleware/security_headers.py`

**Key implementation notes:**
- `auth.py`:
  - Decorators pull token from `Authorization: Bearer <...>` header.
  - Decode, verify `type=access`, load user via `user_repo.get_by_id` (services MAY call this; decorator just attaches `g.current_user_id`, `g.current_user_role`, `g.jwt_jti`).
  - `role_required('admin')` composes on top of `jwt_required`.
  - For internal endpoints: `internal_api_key_required` reads `X-Internal-API-Key` header, constant-time compares to `INTERNAL_API_KEY`.
  - Never dereference `g.current_user` lazily; keep the user id and let services load if they need it.
- `error_handlers.py`:
  - Register on the app: 400 (Marshmallow `ValidationError`), 401, 403, 404, 405, 409, 422, 429, 500.
  - For `marshmallow.ValidationError`, map `err.messages` into `details`.
  - For generic `Exception` handler: log with traceback, return `error_response("INTERNAL_ERROR", "...", status=500)`. Do NOT leak stack traces.
  - For `sqlalchemy.exc.IntegrityError`, translate to `CONFLICT` 409 with message tuned per unique-constraint name if possible.
- `request_id.py`:
  - `before_request`: read `X-Request-ID`, else generate `uuid4().hex`. Store in `g.request_id`.
  - `after_request`: echo `X-Request-ID` header on response.
  - Install a `logging.Filter` that reads `g.request_id` (falling back to `"-"` outside request ctx) and binds it to every `LogRecord.request_id`.
- `security_headers.py`:
  - `after_request` adds: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security: max-age=31536000; includeSubDomains` (prod only), `Cache-Control: no-store` on auth + payment routes (apply via blueprint-level after_request in those blueprints specifically).
  - Do NOT add a default CSP — this is an API, CSP belongs on the Next.js frontend.

**Dependencies on previous waves:** none (this IS the first wave).
**Exit criterion:** `flask --app wsgi run` starts; `curl localhost:5000/api/v1/healthz` returns an envelope (add a tiny `/healthz` in `api/v1/__init__.py` during Wave 1 for smoke-testing).

---

## Wave 2 — Models, Schemas, Migration (PARALLEL within wave)

**Parallel strategy:** All models can be authored in parallel because they are sibling modules. Schemas likewise. The migration step is the one serialization point (runs once all models are in place).

### 2.1 Models (parallel — 7 workers)

**Files to create (one worker per file is ideal):**
- `backend/app/models/__init__.py` — re-export every model class and every enum.
- `backend/app/models/_mixins.py` — `TimestampMixin` (`created_at`, `updated_at` with `server_default=func.now()` and `onupdate=func.now()`).
- `backend/app/models/user.py` — `User`, `AdminProfile`, `UserRole` enum.
- `backend/app/models/hostel.py` — `Hostel`, `HostelImage`, `Amenity`, `HostelAmenity`, `HostelStatus` enum.
- `backend/app/models/room.py` — `Room`, `RoomBlock`, `AvailabilityStatus` enum.
- `backend/app/models/booking.py` — `Booking`, `BookingStatus` enum (string Enum, all 11 states).
- `backend/app/models/payment.py` — `Payment`, `PaymentStatus` enum, `PaymentProvider` enum.
- `backend/app/models/auth_token.py` — `AuthToken`, `PasswordReset`.
- `backend/app/models/audit.py` — `AuditLog` with `metadata` column; name the Python attribute `extra` and map with `Column("metadata", JSONB, ...)` because `metadata` is reserved on SQLAlchemy declarative base.

**Key implementation notes:**
- Use SQLAlchemy 2.0 typed mapped style: `mapped_column()` + `Mapped[...]`. Migrations autogenerate still works; the codebase will look modern.
- Enum columns: use `sa.Enum(MyEnum, name="my_enum", native_enum=True)`. PostgreSQL creates a CHECK-backed TYPE. Always name the type — unnamed enums wreck migrations.
- `bookings.nights_count`: `mapped_column(Integer, Computed("check_out - check_in", persisted=True))`. Alembic will translate to `GENERATED ALWAYS AS ... STORED`. Verify post-autogenerate.
- `bookings.status`: per spec it is `VARCHAR(40)`, not an enum. Use `String(40)` and an application-level `BookingStatus(str, Enum)`. A CHECK constraint enumerating all 11 values is worth adding in Wave 2.3 by hand.
- Add `CheckConstraint("check_out > check_in", name="ck_bookings_dates_order")`, `CheckConstraint("guests_count > 0", name="ck_bookings_guests")` etc., per spec §3.
- `payments`: `UniqueConstraint("provider", "provider_ref", name="uq_payments_provider_ref")` — this is the idempotency key for webhooks.
- Every `ForeignKey` that the spec says CASCADE (e.g., `payments.booking_id`, `rooms.hostel_id`) must specify `ondelete="CASCADE"` in both the FK and a `passive_deletes=True` on the parent `relationship()`.
- Add indexes: `hostels(city)`, `hostels(status)`, `rooms(hostel_id, availability_status)`, `bookings(room_id, check_in, check_out)` (the big one for overlap scans), `bookings(status)`, `bookings(user_id)`, `payments(booking_id)`, `payments(status)`, `audit_logs(entity_type, entity_id)`.
- `AuthToken.refresh_token_hash`: `Text`, indexed (`unique=True, index=True`). Store `sha256(token)` hex. Never store raw tokens.
- `PasswordReset.token_hash`: same pattern, indexed unique.

**Gotchas:**
- `metadata` on any declarative model shadows SQLAlchemy's own `MetaData` attribute. For `AuditLog`, declare the Python attribute as `extra` and map to column `"metadata"` explicitly.
- If you leave `UserRole` and `HostelStatus` etc. as `enum.Enum`, `sa.Enum(UserRole)` stores the enum's NAME by default. Use `values_callable=lambda x: [e.value for e in x]` to store VALUES ("user", "admin") — matches the spec and keeps migrations readable.
- PostgreSQL's generated column (`GENERATED ALWAYS AS ... STORED`) cannot be set in Python; SQLAlchemy's `Computed` handles this correctly but you must omit `nights_count` from all INSERT statements. Don't set it in factories or seeds.

### 2.2 Schemas (parallel — 6 workers, after models exist)

**Files to create:**
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/auth.py` — `RegisterSchema`, `LoginSchema`, `ForgotPasswordSchema`, `ResetPasswordSchema`, `ChangePasswordSchema`, `RefreshResponseSchema`.
- `backend/app/schemas/user.py` — `UserOutSchema`, `UserUpdateSchema`.
- `backend/app/schemas/hostel.py` — `HostelOutSchema`, `HostelListQuerySchema`, `HostelCreateSchema`, `HostelUpdateSchema`, `HostelImageSchema`.
- `backend/app/schemas/room.py` — `RoomOutSchema`, `RoomCreateSchema`, `RoomUpdateSchema`, `RoomBlockCreateSchema`, `RoomBlockOutSchema`.
- `backend/app/schemas/booking.py` — `BookingCreateSchema`, `BookingOutSchema`, `BookingListQuerySchema`, `BookingActionSchema` (for approve/reject with optional `admin_notes`).
- `backend/app/schemas/payment.py` — `PaymentIntentRequestSchema`, `PaymentIntentResponseSchema`, `PaymentOutSchema`, `PaymentRefundSchema`, `PaymentReconcileSchema`.

**Key implementation notes:**
- Use `marshmallow.Schema` with `@validates_schema` for cross-field checks (e.g., `check_out > check_in`). Don't duplicate model-level checks — schema-level errors return 422 with helpful field info; DB-level checks are the last line of defense.
- `UserOutSchema` NEVER exposes `password_hash`. Use explicit `fields.Method` / `only` selection, not `ModelSchema`-style dump-everything.
- Password field: `fields.Str(load_only=True, validate=Length(min=PASSWORD_MIN_LENGTH))`.
- Email: `fields.Email(required=True)` — note marshmallow's email validator does not enforce deliverability; good enough.
- Decimal money fields: `fields.Decimal(as_string=True, places=2)`.
- Pagination query schema (shared): `fields.Int(load_default=1, validate=Range(min=1))`, `per_page` with `Range(min=1, max=100)`.
- `BookingListQuerySchema` — `status` is a `String(validate=OneOf(BookingStatus.values()))`.

**Gotcha:** Marshmallow's `fields.DateTime` defaults to ISO 8601 but will accept naive datetimes and silently pretend they're UTC. Use a custom `fields.AwareDateTime` (ships in marshmallow 3.x) and set `default_timezone=timezone.utc`.

### 2.3 Initial migration (SERIALIZED — single agent, after 2.1 done)

**Steps:**
1. `flask db init` (one-time).
2. `flask db migrate -m "initial schema"`.
3. Manual review of the generated migration:
   - Verify every enum type is created.
   - Verify `bookings.nights_count` is `GENERATED ALWAYS AS (check_out - check_in) STORED`.
   - Add the CHECK constraint enumerating valid `bookings.status` values (autogenerate won't catch it).
   - Verify all CASCADE FKs.
   - Verify every index from 2.1 is present.
4. `flask db upgrade` against dev DB to smoke-test.
5. Commit both the model files and `migrations/versions/<hash>_initial_schema.py`.

**Files produced:** `backend/migrations/versions/<hash>_initial_schema.py`.

**Dependencies on previous waves:** Wave 1 complete (extensions, factory).
**Exit criterion:** `flask db upgrade` against empty DB succeeds; `psql -c "\\dt"` shows all tables.

---

## Wave 3 — Repositories (PARALLEL — 6 workers)

**Parallel strategy:** Each repository is an isolated file. No cross-file imports except models.

### 3.1 Files

- `backend/app/repositories/__init__.py` (empty or expose repo modules)
- `backend/app/repositories/user_repo.py`
- `backend/app/repositories/hostel_repo.py`
- `backend/app/repositories/room_repo.py`
- `backend/app/repositories/booking_repo.py`
- `backend/app/repositories/payment_repo.py`
- `backend/app/repositories/audit_repo.py`

### 3.2 Conventions

- Functions, not classes. `def get_by_id(user_id: int) -> User | None`.
- Repositories NEVER commit. They `db.session.add()` / query / return. Services call `db.session.commit()`.
- Every repo exposes at minimum: `create(**kwargs)`, `get_by_id(id)`, `list(...)`, plus domain-specific finders.
- Queries use SQLAlchemy 2.0 `select(Model).where(...)` style via `db.session.execute(...).scalars()`.

### 3.3 Per-repo critical functions

- **`user_repo`**: `get_by_email`, `get_by_id`, `create`, `update`, `list_admins`, `set_password_hash`.
- **`hostel_repo`**: `search(filters: HostelFilters, page, per_page)` with dynamic `where` clauses. Filters: city (ilike), price range (join rooms, min of room price), availability (subquery excluding rooms booked for date range — or defer availability filter to service because it's expensive). `get_by_id_with_images_and_amenities` (eager-load with `selectinload`). `list_by_admin(admin_user_id)`. `soft_delete(hostel_id)` (sets `status='inactive'`).
- **`room_repo`**:
  - `list_by_hostel`, `get_by_id`, `create`, `update`, `soft_delete` (`availability_status='unavailable'`).
  - **`find_available_room_locked(room_id, check_in, check_out) -> Room | None`** — this is the CRITICAL one: `SELECT ... FROM rooms WHERE id = :room_id AND availability_status = 'available' FOR UPDATE`. Must be called inside an active transaction.
  - `list_blocks_for_room(room_id, date_range)`.
  - `create_block`, `delete_block`.
- **`booking_repo`**:
  - `create`, `get_by_id`, `list_by_user`, `list_admin(filters)`.
  - **`find_overlapping_bookings_locked(room_id, check_in, check_out, excluding_booking_id=None) -> list[Booking]`** — raw overlap predicate: `check_in < :new_check_out AND check_out > :new_check_in` filtered by `status IN ('pending_admin_approval','awaiting_payment','payment_pending','confirmed','checked_in')`. Must use `with_for_update()` on the `rooms` row (via the room lock from `room_repo.find_available_room_locked`), not on `bookings` — locking the parent (room) is what serializes overlap checks. Alternative is `SERIALIZABLE` isolation; we go with pessimistic row-lock.
  - `find_active_blocks_locked(room_id, check_in, check_out)` — overlap against `room_blocks`.
  - `expire_holds(now)` — bulk update bookings where `hold_expires_at < now` and status IN hold-states to `expired`.
- **`payment_repo`**: `create`, `get_by_id`, `get_by_provider_ref(provider, provider_ref)` (for webhook idempotency), `list_by_booking`, `list_admin(filters)`, `update_status`.
- **`audit_repo`**: `log(actor_user_id, entity_type, entity_id, action, extra=None, ip=None)`. Commits in its own sub-transaction? NO — join caller's transaction. If the caller rolls back, audit rolls back too. That's acceptable for v1; emit audit only on the success path in services.

**Dependencies on previous waves:** Wave 2 models.
**Exit criterion:** Each repo has at least a smoke test (lives in Wave 7) or a `python -c "from app.repositories import booking_repo"` import works.

**Gotchas:**
- `with_for_update(of=Room)` requires Postgres 9.3+. It is specifically `SELECT ... FOR UPDATE OF <table>`. Without `of=`, SQLAlchemy emits `FOR UPDATE` against the outermost FROM which locks too much.
- Do NOT put `with_for_update` on a `LEFT OUTER JOIN` — Postgres rejects.
- Keep `hostel_repo.search` availability filtering OUT of the repo SQL for v1; filter in-memory after paginating or via a subquery. Price filter: `EXISTS (SELECT 1 FROM rooms r WHERE r.hostel_id = h.id AND r.price_per_night BETWEEN :min AND :max)`.

---

## Wave 4 — Services (STAGED PARALLEL)

**Parallelism sub-structure:**

**Wave 4a (parallel — 4 workers):**
- `auth_service`, `user_service`, `hostel_service`, `room_service` — these only depend on their own repos + utilities.

**Wave 4b (parallel — 3 workers, after 4a):**
- `audit_service` (standalone on audit_repo; can also go in 4a but `booking_service` imports it in 4c, so do it early).
- `notification_service` (standalone).
- `analytics_service` (depends: booking_repo, payment_repo; no service deps).

**Wave 4c (serialized — 1 worker, after 4a + 4b):**
- `booking_service` (depends: booking_repo, room_repo, audit_service, notification_service).
- `payment_service` (depends: payment_repo, booking_service, payment adapters — blocked until Wave 5).

### 4.1 `auth_service.py`

**Functions:**
- `register_user(payload) -> User` — check email unique, hash password, insert, audit-log, return.
- `login(email, password, user_agent, ip) -> (access_token, refresh_token_raw, user)` — verify, issue tokens, insert `AuthToken` with `refresh_token_hash`.
- `refresh(refresh_token_raw, user_agent, ip) -> (access_token, new_refresh_raw)` — find by hash, check not revoked/expired, revoke old, issue new (rotation).
- `logout(refresh_token_raw)` — mark `revoked_at = now`.
- `forgot_password(email)` — always returns None (no email enumeration). If user exists, generate reset, store hash, send email via `notification_service`.
- `reset_password(raw_token, new_password)` — find by hash, check expires_at/used_at, hash new password, mark reset used, revoke ALL of the user's refresh tokens.
- `change_password(user_id, current_password, new_password)` — verify current, update hash, revoke all refresh tokens except current (optional; v1 may revoke all).

**Gotcha:** Do NOT compare raw tokens directly. Always hash with sha256 then compare by `token_hash` lookup. Timing safety is automatic because DB index lookup is constant-ish.

### 4.2 `user_service.py`

- `get_me(user_id)`, `update_me(user_id, payload)` — disallow updating email/role from here.

### 4.3 `hostel_service.py`

- `search_hostels(filters, page, per_page)`.
- `get_hostel(hostel_id)` — 404 if `status='inactive'` for public callers.
- `admin_create_hostel(admin_user_id, payload)`.
- `admin_update_hostel(hostel_id, payload, actor_user_id)` — enforce ownership (admin_user_id matches actor OR actor is a super-admin; v1: match).
- `admin_soft_delete_hostel(hostel_id, actor_user_id)`.
- `add_image`, `delete_image`.

**Gotcha:** Spec says "soft delete" for hostels — set `status='inactive'`, but existing bookings keep referencing it. Make sure public search excludes `inactive`. Admin list includes them.

### 4.4 `room_service.py`

- `admin_create_room`, `admin_update_room`, `admin_soft_delete_room`.
- `admin_create_block`, `admin_delete_block` — block creation must also check overlap with active bookings; if overlap, 409 with details.

### 4.5 `audit_service.py`

- Thin wrapper; provides `record(actor_user_id, entity_type, entity_id, action, extra=None)` and pulls IP from `flask.request`.

### 4.6 `notification_service.py`

- `send_booking_submitted(user, booking)`, `send_booking_approved`, `send_booking_rejected`, `send_payment_confirmed`, `send_password_reset(user, raw_token)`.
- In dev/test, render subject+body and log (behind `MAIL_SUPPRESS_SEND=True` if desired).
- In prod, use Flask-Mail; wrap sends in `try/except` — a mail failure must NEVER fail the request. Log + continue.

### 4.7 `analytics_service.py`

- `summary(date_from, date_to, granularity, hostel_id=None)`:
  - Revenue (sum of `payments.amount` where `status='success'` in range).
  - Bookings by status (counts).
  - Occupancy rate: (sum of confirmed/checked_in nights in window) / (sum of available room-nights in window).
  - Top hostels by revenue, limit 5.
- Granularity bucketed via `date_trunc('day'|'week'|'month', paid_at)`.

### 4.8 `booking_service.py` — THE COMPLEX ONE

**Functions:**
- `create_booking(user_id, payload) -> Booking`:
  1. Validate dates (via `utils/dates.py`).
  2. Open transaction.
  3. `room = room_repo.find_available_room_locked(room_id)` — `SELECT ... FOR UPDATE`. If None → 409 `ROOM_UNAVAILABLE`.
  4. Check hostel is active; room's hostel matches payload.hostel_id.
  5. `overlapping = booking_repo.find_overlapping_bookings_locked(room_id, check_in, check_out)`. If any → 409 `ROOM_UNAVAILABLE`.
  6. `blocks = booking_repo.find_active_blocks_locked(room_id, check_in, check_out)`. If any → 409 `ROOM_UNAVAILABLE` with `reason`.
  7. Compute `total_amount = room.price_per_night * nights * guests_count_factor` (spec: guests affects capacity, not price — so `total = price_per_night * nights`; re-read spec §3: no "guests multiplier", so just `price_per_night * nights`).
  8. Insert booking with `status='pending_admin_approval'` and `hold_expires_at = now + HOLD_TTL_MINUTES`.
  9. `audit_service.record(user_id, 'booking', booking.id, 'create')`.
  10. Commit. Send notification. Return.
- `get_booking(booking_id, actor_user_id, actor_role)` — enforce owner-or-admin.
- `list_my_bookings(user_id, filters)`.
- `cancel_booking(booking_id, actor_user_id, actor_role)`:
  - Load booking, enforce owner-or-admin.
  - Guard: status must NOT be `checked_in | checked_out | completed | cancelled | expired | rejected`.
  - Transition to `cancelled`. Audit. Notify.
- `admin_approve(booking_id, admin_user_id, notes=None)`:
  - Must be `pending_admin_approval`. Transition to `awaiting_payment`. Extend `hold_expires_at` by HOLD_TTL (fresh 30min window for payment). Audit. Notify.
- `admin_reject(booking_id, admin_user_id, notes)`: from `pending_admin_approval` to `rejected`.
- `admin_checkin(booking_id, admin_user_id)`: from `confirmed` to `checked_in`.
- `admin_checkout(booking_id, admin_user_id)`: from `checked_in` to `checked_out`.
- `admin_complete(booking_id, admin_user_id)`: from `checked_out` to `completed`.
- `system_start_payment_pending(booking)`: from `awaiting_payment` to `payment_pending` (called by payment_service on intent creation).
- `system_mark_confirmed(booking)`: from `payment_pending` to `confirmed` (called by payment_service on webhook success).
- `system_revert_to_awaiting(booking)`: from `payment_pending` to `awaiting_payment` (webhook failure, user may retry).
- `system_expire_holds() -> int`: bulk transition; returns count. Called by internal endpoint.

**State machine:** A single private helper `_assert_transition(current, target)` with a dict-of-sets `_ALLOWED_TRANSITIONS` mirroring spec §4. Wrong transition raises `InvalidStateTransitionError` → 422 `INVALID_STATE_TRANSITION`.

**Gotchas (critical):**
- Hold the row lock across the entire booking insert. In SQLAlchemy, the transaction is the session itself when `autocommit=False` — do NOT open a nested `db.session.begin()` unless you understand SAVEPOINTs. One `try/commit/except/rollback` around the whole flow.
- `find_overlapping_bookings_locked` must be called AFTER the room is locked. Lock order: `rooms` row → then query `bookings`. This serializes two concurrent requests on the same room.
- `expire_holds` must not race payment webhooks. Because webhooks run in their own request/transaction, and `expire_holds` uses `UPDATE ... WHERE status IN (...) AND hold_expires_at < now`, the window is: (a) webhook moves to `payment_pending` → expire_holds misses it; (b) webhook moves to `confirmed` → expire_holds misses it. Safe. But: if webhook moves from `payment_pending` back to `awaiting_payment` (fail/retry) and the hold has expired in between, the next `expire_holds` pass will expire it. That's desired.
- Never send the notification INSIDE the DB transaction. Collect "events" and emit after commit.

### 4.9 `payment_service.py`

(Depends on Wave 5 adapters — finalize here.)

**Functions:**
- `create_intent(booking_id, user_id) -> dict`:
  1. Load booking, enforce ownership.
  2. Guard: status must be `awaiting_payment`.
  3. Provider = factory.get_provider() per `PAYMENT_PROVIDER`.
  4. `provider.create_intent(booking, booking.total_amount, 'INR', metadata={booking_id, user_id})`.
  5. Insert `Payment` row with status=`pending`, provider, provider_ref.
  6. Transition booking to `payment_pending` via `booking_service.system_start_payment_pending`.
  7. Commit, return `{client_secret_or_equivalent, payment_id}`.
- `handle_webhook(provider_name, headers, raw_body) -> dict`:
  1. `provider = factory.get_provider(provider_name)`.
  2. `event = provider.verify_webhook(headers, raw_body)` — must raise on bad signature, 400 at route.
  3. Idempotency: `payment_repo.get_by_provider_ref(provider_name, event['provider_ref'])`. If found and already in terminal state, return `{status:'duplicate'}` 200.
  4. Update payment row status based on event.
  5. If success: `booking_service.system_mark_confirmed(booking)`. Notify.
  6. If fail: `booking_service.system_revert_to_awaiting(booking)` IF hold not expired; else `expired`.
- `get_status_for_booking(booking_id, actor_user_id, actor_role)`.
- `admin_reconcile(payment_id, actor_user_id)` — re-query provider, update row.
- `admin_refund(payment_id, actor_user_id, amount=None)` — v1 is full refund only (ignore amount); call provider.refund, update status to `refunded`, audit, notify.

**Gotchas (critical):**
- Webhook route MUST receive raw body BEFORE Flask parses JSON. See Wave 6 notes.
- Don't trust `provider_ref` from the HTTP body directly for lookup — use the one extracted by `provider.verify_webhook` after signature check.
- Idempotency hinges on `UNIQUE(provider, provider_ref)`. If a webhook duplicates, `INSERT` fails with IntegrityError — catch and treat as duplicate.

**Dependencies on previous waves:** Waves 2, 3, 5.

---

## Wave 5 — Payment Adapters (PARALLEL — 4 workers)

### 5.1 Files

- `backend/app/payments/__init__.py`
- `backend/app/payments/base.py` — `PaymentProvider` ABC.
- `backend/app/payments/mock.py` — `MockProvider`.
- `backend/app/payments/stripe_provider.py` — stub that raises `NotImplementedError` for create_intent/refund but implements `verify_webhook` scaffolding.
- `backend/app/payments/razorpay_provider.py` — stub, same.
- `backend/app/payments/factory.py` — `get_provider(name: str | None = None) -> PaymentProvider`.

### 5.2 Implementation notes

- `base.PaymentProvider`:
  ```python
  class PaymentProvider(ABC):
      name: ClassVar[str]
      @abstractmethod
      def create_intent(self, booking, amount: Decimal, currency: str, metadata: dict) -> dict: ...
      @abstractmethod
      def verify_webhook(self, headers: Mapping[str, str], raw_body: bytes) -> dict: ...
      @abstractmethod
      def fetch_payment_status(self, provider_ref: str) -> dict: ...
      @abstractmethod
      def refund(self, provider_ref: str, amount: Decimal | None = None) -> dict: ...
  ```
- `MockProvider`:
  - `create_intent`: returns `{provider_ref: uuid4().hex, client_secret: "mock_" + provider_ref, status: "pending"}`.
  - `verify_webhook`:
    - Compute `hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()`.
    - Compare with `headers.get('X-Mock-Signature')` using `hmac.compare_digest`.
    - Parse JSON body; require `{event, provider_ref, status}`. Return normalized `{provider_ref, status, raw: event_dict}`.
  - `fetch_payment_status`: mirrors DB state (mock doesn't actually call anywhere); accept an optional in-memory store or just return `{status:'success'}` for tests — prefer the first.
  - `refund`: returns `{status:'refunded', provider_ref, amount}`.
- `stripe_provider.py` / `razorpay_provider.py`:
  - Imports guarded in try/except so absence of the SDK doesn't break test runs.
  - `create_intent` / `refund` raise `NotImplementedError("Stripe/Razorpay not enabled in v1")`.
  - `verify_webhook` is a structural skeleton (real signature algorithms documented inline with TODO).
- `factory.get_provider`:
  - No-arg form: reads `current_app.config['PAYMENT_PROVIDER']`.
  - With-arg form (used by webhook router): `get_provider('mock' | 'stripe' | 'razorpay')`.
  - Caches per-app.

**Gotchas:**
- Stripe's real `verify_webhook` needs the raw body byte-for-byte — any middleware that parses JSON first breaks this. We enforce raw-body handling at the route layer (Wave 6.5).
- Keep `PaymentProvider.name` as a class var used for reverse lookup (`factory`'s registry).

**Dependencies on previous waves:** none (can actually start in Wave 2 — included here because `payment_service` needs it).

---

## Wave 6 — API Routes (PARALLEL — 7+ workers after Wave 4)

### 6.1 Blueprint wiring

- `backend/app/api/__init__.py` — empty package.
- `backend/app/api/v1/__init__.py` — `api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')`. Import sub-modules at the bottom to register routes. Register one `/healthz` that returns `{status:'ok'}`.

### 6.2 Files (all parallel)

- `backend/app/api/v1/auth.py`
- `backend/app/api/v1/users.py`
- `backend/app/api/v1/hostels.py`
- `backend/app/api/v1/bookings.py`
- `backend/app/api/v1/payments.py`
- `backend/app/api/v1/internal.py`

**Admin routes split into 4 files (all parallel):**
- `backend/app/api/v1/admin/__init__.py` — `admin_bp = Blueprint('admin', __name__, url_prefix='/admin')` (nested under api_v1).
- `backend/app/api/v1/admin/hostels.py` — `/admin/hostels`, `/admin/hostels/<id>`, `/admin/hostels/<id>/images`, `/admin/rooms*`, `/admin/availability/blocks*` (rooms + availability live here because they're hostel-admin-only; or split further if preferred).
- `backend/app/api/v1/admin/bookings.py` — `/admin/bookings*` including approve/reject/checkin/checkout/complete.
- `backend/app/api/v1/admin/payments.py` — `/admin/payments*` including reconcile/refund.
- `backend/app/api/v1/admin/analytics.py` — `/admin/analytics/summary`.

### 6.3 Route conventions

- Every route: `@api_v1.route(...)`, then `@jwt_required` / `@role_required('admin')`, then (last) `@limiter.limit(...)` if needed.
- Request body: `Schema().load(request.get_json() or {})`. Query: `Schema().load(request.args, partial=False)`.
- Response: `return success_response(data=OutSchema().dump(obj), status=201)` etc.
- Route functions MUST be thin: schema-load → service-call → schema-dump → response. No business logic.

### 6.4 Rate limits (from common patterns, spec §7 has memory backend):

- `/auth/login`: `5/minute;20/hour` per IP.
- `/auth/register`: `10/hour` per IP.
- `/auth/forgot-password`: `3/minute;10/hour` per IP.
- `/auth/reset-password`: `5/minute` per IP.
- `/payments/webhook/<provider>`: NO rate limit (provider controls rate).
- Everything else: global default from config (say `1000/hour` per IP for authenticated, `300/hour` for anon).

### 6.5 Webhook route — the critical gotcha

- Path: `POST /api/v1/payments/webhook/<provider>`.
- Implementation order INSIDE the view function:
  1. `raw_body = request.get_data(cache=True, as_text=False)` — bytes, BEFORE anything touches `request.get_json()` or `request.form`.
  2. `headers = request.headers` (case-insensitive mapping).
  3. Delegate to `payment_service.handle_webhook(provider, headers, raw_body)`.
  4. On signature failure: return `error_response("UNAUTHORIZED", ..., status=401)` (or 400; Stripe docs prefer 400).
  5. Return 200 even for duplicate/idempotent events — providers retry on non-2xx.
- Route MUST NOT call `request.get_json()` at any point. If it does, the raw body is consumed and HMAC verification fails.
- Exempt this route from CSRF if CSRF is ever added. Exempt from the global JSON parser. Ensure no `before_request` on the auth blueprint accidentally parses.

### 6.6 Internal route

- `POST /api/v1/internal/expire-holds`:
  - `@internal_api_key_required`.
  - Calls `booking_service.system_expire_holds()`.
  - Returns `{expired_count: N}`.

**Dependencies on previous waves:** Wave 4 services.
**Exit criterion:** All routes return documented shape; manual smoke-test of end-to-end booking flow via `curl` works.

---

## Wave 7 — Tests (PARALLEL — many workers)

### 7.1 Test infrastructure (SERIALIZED first)

**Files:**
- `backend/tests/__init__.py`
- `backend/tests/conftest.py`
- `backend/tests/factories.py` — factory-boy factories for User, Hostel, Room, Booking, Payment.

**conftest.py essentials:**
- `app` fixture (session scope): `create_app('testing')`; push app context.
- `db` fixture (session scope): creates schema once; teardown drops all.
- `session` fixture (function scope): opens nested transaction, yields `db.session`, rolls back. This makes every test hermetic. Use SQLAlchemy's `SAVEPOINT` via `connection.begin_nested()` pattern.
- `client` fixture (function scope): `app.test_client()`.
- `auth_headers_user(user_factory)` and `auth_headers_admin(...)` helpers: create user, hit `/auth/login`, return `{'Authorization': f'Bearer {token}'}`.
- `freezer` fixture wrapping `freezegun.freeze_time`.

**Gotcha:** If a test creates a booking and a payment webhook fires in the same test, the SAVEPOINT-per-test pattern will NOT roll back changes made in a second connection. For integration tests needing realistic isolation, use a `truncate_all` fixture instead.

### 7.2 Unit tests (parallel)

- `backend/tests/unit/test_password.py` — hash/verify, wrong password, deterministic length.
- `backend/tests/unit/test_tokens.py` — encode/decode, expiry (with freezegun), tamper detection, wrong `type`.
- `backend/tests/unit/test_booking_state_machine.py` — every legal transition, every illegal transition raises.
- `backend/tests/unit/test_overlap_detection.py` — half-open interval math, edge cases: identical dates (touching), containment, partial overlap both directions.
- `backend/tests/unit/test_payment_mock.py` — HMAC signature verify good+bad, create_intent shape, refund shape.

### 7.3 API tests (parallel)

- `backend/tests/api/test_auth.py` — register, login (good/bad), refresh rotation, forgot+reset full cycle, logout revocation.
- `backend/tests/api/test_hostels.py` — list with filters, pagination, detail, 404 on inactive.
- `backend/tests/api/test_bookings.py` — create happy path, create with overlap (expect 409), create with expired hold, cancel own, cancel other's (403), list `/my`.
- `backend/tests/api/test_payments.py` — create intent (happy), webhook success → booking confirmed, webhook duplicate → idempotent, webhook bad signature → 401, status query.
- `backend/tests/api/test_admin_hostels.py` — CRUD, image add/remove, RBAC.
- `backend/tests/api/test_admin_bookings.py` — approve, reject, checkin→checkout→complete, illegal transitions 422.
- `backend/tests/api/test_rbac.py` — matrix: for each admin endpoint, user role returns 403; unauth returns 401.

### 7.4 Integration (1 test)

- `backend/tests/integration/test_booking_flow.py` — end-to-end: register user → admin creates hostel+room → user searches → user books → admin approves → user pays (mock webhook) → booking confirmed → admin checkin → checkout → complete. Assert audit log populated and notification functions invoked (monkey-patch to capture).

### 7.5 Coverage targets (from spec §8)

- Overall: 80% minimum — enforce via `--cov-fail-under=80` in CI config (not pytest.ini, so dev runs don't fail).
- 90% on: `app/services/booking_service.py`, `app/payments/`, `app/middleware/auth.py` — add specific coverage assertions in CI.

**Dependencies on previous waves:** Waves 1–6.
**Exit criterion:** `pytest -q` green locally; coverage thresholds met.

---

## Cross-Wave Gotchas (consolidated)

1. **Booking overlap lock**: Always `SELECT ... FOR UPDATE OF rooms` before reading bookings. Without it, two concurrent bookings on the same room for the same dates both succeed. Test this with a threaded pytest scenario or document as manual QA.
2. **Webhook raw body**: Read `request.get_data(cache=True, as_text=False)` FIRST. Do not call `request.get_json()` anywhere before HMAC verification.
3. **JWT sub claim must be a string**: PyJWT ≥ 2.10 rejects non-string `sub`.
4. **passlib + bcrypt version**: Pin `bcrypt<4.1` or passlib blows up with `__about__` attribute error.
5. **SQLAlchemy `metadata` attribute**: `AuditLog` cannot use `metadata` as a Python attribute name; map column explicitly.
6. **CORS + credentials**: Exact origins list, never `*`, when `supports_credentials=True`.
7. **Flask-Mail failures**: Never fail a request because mail failed. Wrap and log.
8. **expire_holds race with webhooks**: Status-set filter in the UPDATE ensures correctness; document the invariant in `booking_service` docstring.
9. **Generated column `nights_count`**: Never insert into it. Never set it in factories.
10. **Marshmallow DateTime naive vs aware**: Force `default_timezone=timezone.utc`.
11. **Enum storage**: Use `values_callable` to store enum values, not names.
12. **Soft-deleted hostels**: Public queries filter; admin queries don't. Don't rely on DB-level default.
13. **Refresh token rotation**: Old token MUST be marked `revoked_at` before new one is returned. If the handler crashes between those two ops, the user has no working token — acceptable; they re-login.
14. **Internal API key check**: Use `hmac.compare_digest`, not `==`.
15. **Decimal everywhere for money**: `float * int` for `total_amount` will introduce 0.01-cent drift and break reconciliation.

---

## Suggested Parallelization Schedule (human-readable timeline)

| Wave | Parallel workers | Serial dependencies | Est. scope |
|---|---|---|---|
| 1 | 1 | — | scaffold + config + extensions + factory + utils + middleware |
| 2 | 7 (models) + 6 (schemas) | then 1 (migration) | parallel authoring, single migration commit |
| 3 | 6 | needs Wave 2 | one worker per repo |
| 4a | 4 | needs Wave 3 | auth, user, hostel, room services |
| 4b | 3 | needs Wave 3 | audit, notification, analytics |
| 5 | 4 | none (can start in parallel with Wave 3) | payment adapters |
| 4c | 1 booking_service + 1 payment_service | needs 4a/4b + 5 | the complex ones |
| 6 | 7+ | needs Wave 4 | all route files parallel |
| 7 | many | needs Wave 6 | unit + api + integration |

**Critical path length:** Wave 1 → Wave 2 (models+migration) → Wave 3 (repos) → Wave 4c (booking+payment) → Wave 6 (routes that use them) → Wave 7 (tests).

---

## Exit Criteria for the Whole Backend

- `flask db upgrade` runs cleanly against a fresh Postgres.
- `pytest --cov=app` reports ≥ 80% overall, ≥ 90% on booking_service + payments/ + middleware/auth.py.
- `make run` serves the API; `/api/v1/healthz` returns envelope.
- End-to-end booking flow (integration test) passes.
- `scripts/seed.py` creates an admin user, one hostel, two rooms; `scripts/expire_holds.py` invokes the internal endpoint successfully.
- No secrets in `.env.example`.
- No route bypasses the response envelope.
- No service commits inside a route handler (repos + services own transactions).
