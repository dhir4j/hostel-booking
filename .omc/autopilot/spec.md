# Backend Technical Specification — Hostel Management Flask API

**Scope:** Backend only (Flask REST API). Target path: `/home/dhir4j/Documents/Dhillon/hostel-application/backend/`.
**Stack:** Python 3.11+, Flask, SQLAlchemy, Flask-Migrate (Alembic), PostgreSQL, PyJWT, bcrypt, Marshmallow for schemas, Flask-Limiter, Flask-CORS, pytest.

## Open Questions — Resolved (v1 defaults)

- **Auto-approve hostels**: `auto_approve: Boolean default False` on hostels table. Booking always starts `pending_admin_approval`.
- **Hold TTL**: 30 minutes.
- **Currency**: INR only for v1. Per-hostel currency deferred.
- **Email verification**: Skip for v1. `email_verified_at` deferred.
- **Admin creation**: Seed script only. No self-register as admin. No admin-users endpoint in v1.
- **Image storage**: URL-based only. Admin provides `image_url`. No file upload in v1.
- **Soft delete**: Hostels and rooms use soft-delete (`status=inactive`). Active bookings preserved but no new bookings allowed on inactive rooms.
- **Cancellation policy**: User can cancel if booking not yet `checked_in`. No automatic refund in v1. Admin triggers refund manually.
- **Partial refund**: Full refund only in v1.
- **completed trigger**: Admin-explicit only in v1.
- **btree_gist**: Use app-level `SELECT ... FOR UPDATE` locking only. No exclusion constraint (safer for PythonAnywhere).
- **Rate limiting**: Memory backend for v1. Redis optional via `RATELIMIT_STORAGE_URI`.
- **Background jobs**: No Celery. Cron via PythonAnywhere scheduled tasks. Simple cleanup endpoint `POST /api/v1/internal/expire-holds` called by cron.
- **Notifications**: Email only in v1.
- **On-behalf booking by admin**: Not in v1.

---

## 1. Folder Structure (exact)

```
backend/
├── app/
│   ├── __init__.py                  # create_app() factory
│   ├── extensions.py                # db, migrate, limiter, mail, cors singletons
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py          # api_v1 blueprint, /api/v1 prefix
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── hostels.py
│   │       ├── bookings.py
│   │       ├── payments.py
│   │       ├── admin.py
│   │       └── internal.py          # expire-holds cron endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # User, AdminProfile
│   │   ├── hostel.py                # Hostel, HostelImage, Amenity, HostelAmenity
│   │   ├── room.py                  # Room, RoomBlock
│   │   ├── booking.py               # Booking, BookingStatus enum
│   │   ├── payment.py               # Payment, PaymentStatus, Provider enums
│   │   ├── auth_token.py            # AuthToken, PasswordReset
│   │   └── audit.py                 # AuditLog
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── hostel_service.py
│   │   ├── room_service.py
│   │   ├── booking_service.py
│   │   ├── payment_service.py
│   │   ├── notification_service.py
│   │   ├── audit_service.py
│   │   └── analytics_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   ├── hostel_repo.py
│   │   ├── room_repo.py
│   │   ├── booking_repo.py
│   │   ├── payment_repo.py
│   │   └── audit_repo.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py                  # jwt_required, role_required
│   │   ├── error_handlers.py
│   │   ├── request_id.py
│   │   └── security_headers.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── hostel.py
│   │   ├── room.py
│   │   ├── booking.py
│   │   └── payment.py
│   ├── payments/
│   │   ├── __init__.py
│   │   ├── base.py                  # PaymentProvider ABC
│   │   ├── mock.py
│   │   ├── stripe_provider.py
│   │   ├── razorpay_provider.py
│   │   └── factory.py
│   └── utils/
│       ├── __init__.py
│       ├── responses.py             # success_response, error_response
│       ├── pagination.py
│       ├── password.py              # bcrypt hash/verify
│       ├── tokens.py                # JWT encode/decode, reset token
│       └── dates.py                 # date validation, overlap check
├── migrations/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_password.py
│   │   ├── test_tokens.py
│   │   ├── test_booking_state_machine.py
│   │   ├── test_overlap_detection.py
│   │   └── test_payment_mock.py
│   ├── api/
│   │   ├── test_auth.py
│   │   ├── test_hostels.py
│   │   ├── test_bookings.py
│   │   ├── test_payments.py
│   │   ├── test_admin_hostels.py
│   │   ├── test_admin_bookings.py
│   │   └── test_rbac.py
│   └── integration/
│       └── test_booking_flow.py
├── scripts/
│   ├── seed.py
│   └── expire_holds.py
├── .env.example
├── .flaskenv
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Makefile
└── wsgi.py
```

---

## 2. API Endpoints (complete)

### Response Envelope
```json
{ "success": true, "data": {}, "error": null, "meta": {} }
```

### Auth `/api/v1/auth`
| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/register` | none | `{full_name, email, phone?, password}` → `{user}` 201 |
| POST | `/login` | none | `{email, password}` → `{access_token, user}` + refresh cookie |
| POST | `/refresh` | cookie | → `{access_token}` + new refresh cookie |
| POST | `/logout` | access | revoke refresh, clear cookie |
| POST | `/forgot-password` | none | `{email}` → always 200 |
| POST | `/reset-password` | none | `{token, new_password}` → 200 |

### Users `/api/v1/users`
| Method | Path | Auth |
|---|---|---|
| GET | `/me` | user/admin |
| PATCH | `/me` | user/admin |
| POST | `/me/change-password` | user/admin |

### Public Hostels `/api/v1/hostels`
| Method | Path | Auth |
|---|---|---|
| GET | `/` | public | `?city&min_price&max_price&check_in&check_out&guests&page&per_page` |
| GET | `/{hostel_id}` | public |

### Bookings `/api/v1/bookings`
| Method | Path | Auth |
|---|---|---|
| POST | `/` | user | `{hostel_id, room_id, check_in, check_out, guests_count}` → 201 |
| GET | `/my` | user/admin | `?status&page` |
| GET | `/{booking_id}` | owner/admin |
| POST | `/{booking_id}/cancel` | owner/admin |

### Payments `/api/v1/payments`
| Method | Path | Auth |
|---|---|---|
| POST | `/create-intent` | user (owner) | `{booking_id}` |
| POST | `/webhook/{provider}` | signature | raw body |
| GET | `/{booking_id}/status` | owner/admin |

### Admin `/api/v1/admin` (role=admin)

**Hostels**
- GET/POST `/hostels`
- GET/PATCH/DELETE `/hostels/{id}`
- POST/DELETE `/hostels/{id}/images`

**Rooms**
- GET/POST `/rooms` (`?hostel_id=`)
- GET/PATCH/DELETE `/rooms/{id}`

**Bookings**
- GET `/bookings` (`?status&hostel_id&user_id&from&to&page`)
- GET `/bookings/{id}`
- POST `/bookings/{id}/approve`
- POST `/bookings/{id}/reject`
- POST `/bookings/{id}/checkin`
- POST `/bookings/{id}/checkout`
- POST `/bookings/{id}/complete`

**Availability**
- GET/POST `/availability/blocks`
- DELETE `/availability/blocks/{id}`

**Payments**
- GET `/payments` (`?status&from&to&page`)
- GET `/payments/{id}`
- POST `/payments/{id}/reconcile`
- POST `/payments/{id}/refund`

**Analytics**
- GET `/analytics/summary` (`?from&to&granularity=daily|weekly|monthly`)

### Internal
- POST `/api/v1/internal/expire-holds` (INTERNAL_API_KEY header)

---

## 3. Database Models

All inherit `TimestampMixin` (created_at, updated_at).

### users
- id BIGSERIAL PK
- full_name VARCHAR(120)
- email VARCHAR(255) UNIQUE
- phone VARCHAR(30) nullable
- password_hash TEXT
- role ENUM('user','admin') default 'user'
- is_active BOOLEAN default True

### admin_profiles
- id PK, user_id BIGINT UNIQUE FK users.id
- organization VARCHAR(150)

### hostels
- id, admin_user_id FK users.id
- name VARCHAR(150), description TEXT, city VARCHAR(80), address TEXT
- latitude NUMERIC(9,6), longitude NUMERIC(9,6)
- status ENUM('active','inactive') default 'active'
- auto_approve BOOLEAN default False

### hostel_images
- id, hostel_id FK, image_url TEXT, is_primary BOOLEAN, sort_order INT

### amenities: id, name UNIQUE
### hostel_amenities: hostel_id + amenity_id composite PK

### rooms
- id, hostel_id FK CASCADE
- room_number VARCHAR(30), room_type VARCHAR(50)
- capacity SMALLINT CHECK>0
- price_per_night NUMERIC(10,2) CHECK>=0
- availability_status ENUM('available','unavailable','maintenance')
- UNIQUE(hostel_id, room_number)

### room_blocks
- id, room_id FK, start_date DATE, end_date DATE, reason VARCHAR(200)
- CHECK end_date > start_date

### bookings
- id, user_id FK, hostel_id FK, room_id FK
- check_in DATE, check_out DATE
- CHECK check_out > check_in
- guests_count SMALLINT CHECK>0
- nights_count INT GENERATED ALWAYS AS (check_out - check_in) STORED
- total_amount NUMERIC(10,2)
- status VARCHAR(40)
- admin_notes TEXT
- hold_expires_at TIMESTAMPTZ nullable

### payments
- id, booking_id FK CASCADE
- provider ENUM('mock','stripe','razorpay')
- provider_ref VARCHAR(120) nullable
- amount NUMERIC(10,2), currency VARCHAR(10) default 'INR'
- status ENUM('pending','success','failed','refunded')
- failure_reason TEXT, paid_at TIMESTAMPTZ
- UNIQUE(provider, provider_ref)

### auth_tokens
- id, user_id FK, refresh_token_hash TEXT
- issued_at, expires_at, revoked_at nullable
- user_agent VARCHAR(255), ip VARCHAR(45)

### password_resets
- id, user_id FK, token_hash TEXT, expires_at, used_at nullable

### audit_logs
- id, actor_user_id FK nullable
- entity_type VARCHAR(50), entity_id BIGINT
- action VARCHAR(50), metadata JSONB
- ip VARCHAR(45), created_at

---

## 4. Booking State Machine

### States
draft, pending_admin_approval, awaiting_payment, payment_pending, confirmed, checked_in, checked_out, completed, rejected, cancelled, expired

### Transitions
| From | To | Actor |
|---|---|---|
| draft | pending_admin_approval | user |
| pending_admin_approval | awaiting_payment | admin |
| pending_admin_approval | rejected | admin |
| pending_admin_approval | expired | system |
| awaiting_payment | payment_pending | system/user |
| awaiting_payment | expired | system |
| awaiting_payment | cancelled | user/admin |
| payment_pending | confirmed | system (webhook) |
| payment_pending | awaiting_payment | system (webhook fail, retry) |
| payment_pending | cancelled | user/admin |
| payment_pending | expired | system |
| confirmed | checked_in | admin |
| confirmed | cancelled | user/admin |
| checked_in | checked_out | admin |
| checked_out | completed | admin |

Invalid transition → 422 INVALID_STATE_TRANSITION.

---

## 5. Auth Flow

- bcrypt cost 12 via passlib
- Access token: HS256, 15 min, claims: sub, role, iat, exp, jti, type=access
- Refresh token: HS256, 7 days, stored hashed in auth_tokens, HTTP-only cookie
- Rotation: /refresh revokes old token, issues new
- Forgot: sha256(token) stored, 30min expiry, one-time use
- Reset: invalidates all refresh tokens for user

---

## 6. Payment Provider Adapter

```python
class PaymentProvider(ABC):
    def create_intent(self, booking, amount, currency, metadata) -> dict: ...
    def verify_webhook(self, headers, raw_body) -> dict: ...
    def fetch_payment_status(self, provider_ref) -> dict: ...
    def refund(self, provider_ref, amount=None) -> dict: ...
```

MockProvider: HMAC-SHA256 webhook verification via WEBHOOK_SECRET.
Stripe/Razorpay: stubs in v1.

---

## 7. Environment Variables

```
APP_ENV, SECRET_KEY, JWT_SECRET_KEY, JWT_ACCESS_TTL_MINUTES=15
JWT_REFRESH_TTL_DAYS=7, DATABASE_URL, FRONTEND_URL, CORS_ORIGINS
RATELIMIT_STORAGE_URI=memory://, PAYMENT_PROVIDER=mock
WEBHOOK_SECRET, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, RAZORPAY_WEBHOOK_SECRET
MAIL_SERVER, MAIL_PORT=587, MAIL_USERNAME, MAIL_PASSWORD
MAIL_FROM=no-reply@hostel.app, MAIL_USE_TLS=true
HOLD_TTL_MINUTES=30, PASSWORD_RESET_TTL_MINUTES=30
PASSWORD_MIN_LENGTH=8, LOG_LEVEL=INFO, INTERNAL_API_KEY
```

---

## 8. Testing Requirements

- pytest + pytest-flask + pytest-cov + freezegun
- Test DB: separate postgres (configurable via TEST_DATABASE_URL)
- Unit: password, tokens, state machine, overlap, mock provider
- API: all endpoints, RBAC matrix, error shapes
- Integration: full booking flow
- Coverage: 80% minimum; 90% on booking_service, payments/, middleware/auth.py
