# Product Requirements Document (PRD)
## Product
Hostel Management Web Application

## Version
1.0 (Production-Ready Baseline)

## Date
April 19, 2026

## Owner
Product + Engineering

---

## 1. Executive Summary
Build a full-stack hostel management platform where:
- Guests can discover hostels and availability.
- Registered users can book and pay online.
- Admins (hostel owners/managers) can manage hostels, rooms, bookings, availability, and payments.

### Mandatory Tech Stack
- Backend: Python `Flask` (REST API)
- Frontend: `Next.js` (latest stable, `App Router`)
- Database: `PostgreSQL`
- Backend Hosting: `PythonAnywhere`
- Frontend Hosting: `Vercel`

---

## 2. Objectives and Success Metrics
### Business Objectives
- Digitize hostel booking and operations.
- Increase occupancy and booking conversion.
- Reduce manual booking/payment reconciliation.

### Product Objectives
- Real-time availability checks with double-booking prevention.
- End-to-end booking and payment workflow.
- Admin-first operational controls with auditability.

### Success Metrics (First 90 days post-launch)
- Booking conversion rate: `>= 3.5%` from hostel detail views.
- Payment success rate: `>= 92%`.
- Double-booking incidents: `0`.
- Admin action SLA (accept/reject): median `< 2 hours`.
- Uptime: `>= 99.5%`.

---

## 3. Scope
### In Scope (MVP+)
- User auth (email/password + JWT + forgot/reset).
- Hostel listing/search/detail views.
- Booking lifecycle with approval and payment.
- Admin panel for hostel/room/booking/payment/availability management.
- Payment gateway integration (mock + Stripe/Razorpay-ready adapter).
- Analytics summary for admin dashboard.

### Out of Scope (Phase 2+)
- Multi-currency settlement engine.
- Advanced recommendation ML.
- Native mobile app.
- Complex refund automation beyond manual/admin-triggered flow.

---

## 4. User Personas
### 1) Guest User (Not Logged In)
- Wants to browse hostels, compare price/location, check availability.
- Cannot place booking without registering.

### 2) Registered User (Customer)
- Wants fast booking, secure payment, and booking history.
- Can manage profile and view booking/payment statuses.

### 3) Admin (Hostel Owner/Manager)
- Wants full inventory and booking control.
- Needs room/date blocking, booking approvals, payment visibility, and occupancy/revenue metrics.

---

## 5. Role Permissions Matrix
| Capability | Guest | Registered User | Admin |
|---|---:|---:|---:|
| View landing page & featured hostels | ✅ | ✅ | ✅ |
| Search hostels | ✅ | ✅ | ✅ |
| View hostel details | ✅ | ✅ | ✅ |
| Create account / login | ✅ | ✅ | ✅ |
| Create booking request | ❌ | ✅ | ✅ (on behalf, optional) |
| Make payment | ❌ | ✅ | ✅ (manual settlement, optional) |
| View own booking history | ❌ | ✅ | ❌ |
| Manage own profile | ❌ | ✅ | ✅ (own account) |
| Manage hostels/rooms | ❌ | ❌ | ✅ |
| Approve/reject bookings | ❌ | ❌ | ✅ |
| Check-in/check-out update | ❌ | ❌ | ✅ |
| View all transactions | ❌ | ❌ | ✅ |
| Block/unblock rooms by date | ❌ | ❌ | ✅ |
| View admin analytics | ❌ | ❌ | ✅ |

---

## 6. Functional Requirements

## 6.1 Authentication & Authorization
### Requirements
- Email/password registration and login.
- JWT-based auth:
  - Access token (short TTL, e.g., 15 min).
  - Refresh token (long TTL, e.g., 7–30 days, rotate on use).
- Role-based access control (`guest`, `user`, `admin`).
- Forgot password flow:
  - Request reset link/token.
  - Token expiry (e.g., 30 minutes).
  - One-time use token.

### Acceptance Criteria
- Unauthorized routes return `401`.
- Role violations return `403`.
- Passwords are hashed with `bcrypt`/`argon2`.
- Reset token cannot be reused or used post-expiry.

---

## 6.2 Frontend Requirements (Next.js App Router)
### UX Standards
- Responsive mobile-first layout.
- Search/filter interaction under 300ms (excluding network).
- Clear booking state transitions and payment feedback.
- Accessible UI (WCAG AA baseline: contrast, keyboard nav, labels).

### Page Breakdown
#### A) Landing Page (`/`)
- Hero section with value proposition + CTA.
- Search module:
  - Location (city/autocomplete optional).
  - Price range.
  - Date range (check-in/check-out).
  - Guests count.
- Featured hostels carousel/grid.
- CTA block: login/register.

#### B) User Auth Pages
- `/register`: name, email, phone(optional), password, confirm.
- `/login`: email/password; forgot password link.
- `/forgot-password`: email input.
- `/reset-password/[token]`: new password form.

#### C) User Experience Pages
- `/dashboard`: quick stats (upcoming booking, pending payments, recent bookings).
- `/hostels`: browse/search/filter/sort/listing cards.
- `/hostels/[id]`: hostel details, amenities, room options, pricing, gallery, map (optional).
- `/booking/[hostelId]`: select room, dates, guest count, pricing summary, policy consent.
- `/payment/[bookingId]`: payment initiation + status poll/result.
- `/bookings`: booking history and status timeline.
- `/profile`: update user details and password change.

#### D) Admin Panel (Detailed)
- Route group: `/admin/*` (protected by admin RBAC).

##### 1. Hostel Management (`/admin/hostels`)
- Add/Edit/Delete hostels.
- Fields: name, description, city, address, coordinates(optional), amenities, images.
- Image upload with preview + main cover image.
- Status: active/inactive.

##### 2. Room Management (`/admin/rooms`)
- Add/Edit/Delete rooms per hostel.
- Fields: room number, type, capacity, base price, availability status.
- Optional bed count and gender policy.

##### 3. Booking Management (`/admin/bookings`)
- View all bookings with filters (date/status/hostel/user).
- Accept/Reject booking requests.
- Set check-in/check-out states.
- View booking timeline/audit.

##### 4. Payment Management (`/admin/payments`)
- Transaction list with filters.
- Status badges: pending/success/failed/refunded.
- Manual reconcile action (if webhook delays).
- Refund trigger (optional, gateway-dependent).

##### 5. Availability Control (`/admin/availability`)
- Block/unblock room inventory for date ranges.
- Reason logging (maintenance/private hold/overbook protection).
- Real-time availability impact reflected in user search and booking.

##### 6. Admin Analytics (`/admin/analytics`)
- Total bookings (daily/weekly/monthly).
- Revenue trend.
- Occupancy rate.
- Pending approvals and payment failures.

---

## 7. System Flows (Mandatory)

## 7.1 User Registration -> Login
1. User opens `/register` and submits form.
2. Backend validates input and creates user record.
3. Optional email verification sent.
4. User logs in via `/login`.
5. Backend issues JWT access + refresh tokens.
6. Frontend stores access token in memory and refresh token in secure HTTP-only cookie.

## 7.2 Search -> Select Hostel -> Book
1. User searches by location/date/price.
2. Backend returns filtered hostels with availability summary.
3. User opens hostel details and chooses room + dates.
4. Booking request is submitted.
5. Backend performs atomic availability validation.
6. Booking created in `pending_admin_approval` (or `awaiting_payment` for auto-approve hostels).

## 7.3 Admin Approval/Rejection
1. Admin reviews pending booking list.
2. Admin accepts or rejects.
3. If accepted: booking state moves to `awaiting_payment` (or `confirmed` if payment already captured).
4. If rejected: state moves to `rejected`, release held inventory.
5. User receives notification (email/in-app).

## 7.4 Payment Process
1. User opens payment page for approved booking.
2. Frontend creates payment intent/order via backend.
3. User completes payment on gateway (Stripe/Razorpay).
4. Gateway sends webhook to backend.
5. Backend verifies signature, updates payment status.
6. Booking state updated (`confirmed` if payment success).

## 7.5 Booking Confirmation
1. Successful payment triggers booking confirmation.
2. Confirmation details available in user dashboard/history.
3. Check-in/check-out managed by admin.
4. Completed stay moves booking to `completed`.

---

## 8. Backend Requirements (Flask)

## 8.1 API Architecture
### Style
- RESTful JSON APIs, versioned: `/api/v1`.
- Stateless auth via JWT.
- Standard response envelope:
```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {}
}
```

### Route Grouping
- `/api/v1/auth/*`
- `/api/v1/users/*`
- `/api/v1/hostels/*`
- `/api/v1/bookings/*`
- `/api/v1/payments/*`
- `/api/v1/admin/*`

## 8.2 Core Modules
- Auth module: register/login/refresh/logout/forgot/reset/RBAC decorators.
- User module: profile CRUD, booking history.
- Hostel module: hostel CRUD, amenity/image metadata, public listing/search.
- Room module: room CRUD, per-date inventory checks.
- Booking engine: lifecycle transitions, concurrency-safe availability checks.
- Payment module: mock provider + provider adapter (`stripe`, `razorpay`) + webhook processing.
- Notification module (baseline): email confirmations and status updates.
- Audit module: capture admin actions and booking/payment state changes.

---

## 9. Booking Logic (Important)
### Key Rules
- No overlapping confirmed/held bookings for same room and date range.
- Date logic:
  - `check_in` is inclusive.
  - `check_out` is exclusive.
- Booking can only move through valid state transitions.

### Suggested Booking States
- `draft`
- `pending_admin_approval`
- `awaiting_payment`
- `payment_pending`
- `confirmed`
- `checked_in`
- `checked_out`
- `completed`
- `rejected`
- `cancelled`
- `expired`

### Double Booking Prevention
- Use DB transaction + row-level locking (`SELECT ... FOR UPDATE`) on room inventory rows or booking-range validation.
- Enforce overlap constraint (recommended via PostgreSQL exclusion constraint where feasible).
- On race condition, return `409 Conflict`.

### Availability Check Algorithm
1. Validate date range and room capacity.
2. Check admin block table for overlap.
3. Check existing active bookings for overlap.
4. Temporarily hold (TTL) or create pending booking.
5. Release hold automatically on timeout/failure.

---

## 10. Database Schema (PostgreSQL)

## 10.1 Entity Relationship Summary
- One `admin` user can manage many `hostels`.
- One `hostel` has many `rooms`.
- One `user` has many `bookings`.
- One `booking` belongs to one `room` and one `hostel`.
- One `booking` can have many `payments` attempts.
- Room-date blocks maintained in `room_blocks`.

## 10.2 Tables and Constraints
| Table | Key Columns | Relationships | Critical Constraints |
|---|---|---|---|
| `users` | `id`, `email`, `password_hash`, `role` | 1:N with bookings | `email UNIQUE`, role CHECK |
| `admin_profiles` | `id`, `user_id`, `organization` | 1:1 with users(admin) | `user_id UNIQUE FK users(id)` |
| `hostels` | `id`, `admin_user_id`, `name`, `city`, `address` | N:1 users(admin), 1:N rooms | `admin_user_id FK users(id)` |
| `hostel_images` | `id`, `hostel_id`, `image_url`, `is_primary` | N:1 hostels | FK + index hostel |
| `amenities` | `id`, `name` | M:N via hostel_amenities | `name UNIQUE` |
| `hostel_amenities` | `hostel_id`, `amenity_id` | join table | composite PK |
| `rooms` | `id`, `hostel_id`, `room_number`, `capacity`, `price_per_night` | N:1 hostels, 1:N bookings | unique(hostel_id, room_number) |
| `room_blocks` | `id`, `room_id`, `start_date`, `end_date`, `reason` | N:1 rooms | date range validity CHECK |
| `bookings` | `id`, `user_id`, `hostel_id`, `room_id`, dates, `status` | N:1 users/hostels/rooms | overlap protection + status CHECK |
| `payments` | `id`, `booking_id`, `provider`, `provider_ref`, amount, `status` | N:1 bookings | idempotency on provider_ref |
| `auth_tokens` | `id`, `user_id`, `refresh_token_hash`, expiry | N:1 users | revoke + expiry index |
| `password_resets` | `id`, `user_id`, `token_hash`, expiry, used_at | N:1 users | one-time use |
| `audit_logs` | `id`, actor_user_id, entity, action, metadata | optional polymorphic refs | immutable append-only |

## 10.3 SQL Sketch (Core Tables)
```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone VARCHAR(30),
  password_hash TEXT NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user','admin')),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE hostels (
  id BIGSERIAL PRIMARY KEY,
  admin_user_id BIGINT NOT NULL REFERENCES users(id),
  name VARCHAR(150) NOT NULL,
  description TEXT,
  city VARCHAR(80) NOT NULL,
  address TEXT NOT NULL,
  latitude NUMERIC(9,6),
  longitude NUMERIC(9,6),
  status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE rooms (
  id BIGSERIAL PRIMARY KEY,
  hostel_id BIGINT NOT NULL REFERENCES hostels(id) ON DELETE CASCADE,
  room_number VARCHAR(30) NOT NULL,
  room_type VARCHAR(50),
  capacity SMALLINT NOT NULL CHECK (capacity > 0),
  price_per_night NUMERIC(10,2) NOT NULL CHECK (price_per_night >= 0),
  availability_status VARCHAR(20) NOT NULL DEFAULT 'available'
    CHECK (availability_status IN ('available','unavailable','maintenance')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(hostel_id, room_number)
);

CREATE TABLE bookings (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  hostel_id BIGINT NOT NULL REFERENCES hostels(id),
  room_id BIGINT NOT NULL REFERENCES rooms(id),
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  guests_count SMALLINT NOT NULL CHECK (guests_count > 0),
  nights_count INT GENERATED ALWAYS AS (check_out - check_in) STORED,
  total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
  status VARCHAR(40) NOT NULL,
  admin_notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (check_out > check_in)
);

CREATE TABLE payments (
  id BIGSERIAL PRIMARY KEY,
  booking_id BIGINT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  provider VARCHAR(30) NOT NULL CHECK (provider IN ('mock','stripe','razorpay')),
  provider_ref VARCHAR(120),
  amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
  currency VARCHAR(10) NOT NULL DEFAULT 'INR',
  status VARCHAR(20) NOT NULL CHECK (status IN ('pending','success','failed','refunded')),
  failure_reason TEXT,
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(provider, provider_ref)
);
```

### Recommended Indexes
- `bookings(room_id, check_in, check_out, status)`
- `bookings(user_id, created_at DESC)`
- `bookings(hostel_id, status, created_at DESC)`
- `hostels(city, status)`
- `rooms(hostel_id, availability_status)`
- `payments(booking_id, status, created_at DESC)`

---

## 11. API Design (Examples)

## 11.1 Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `POST /api/v1/auth/logout`

Example `POST /api/v1/auth/login` request:
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

Example response:
```json
{
  "success": true,
  "data": {
    "access_token": "jwt_access_token",
    "user": {
      "id": 101,
      "full_name": "A User",
      "email": "user@example.com",
      "role": "user"
    }
  }
}
```

## 11.2 Public Hostels
- `GET /api/v1/hostels?city=&min_price=&max_price=&check_in=&check_out=&guests=`
- `GET /api/v1/hostels/{hostel_id}`

## 11.3 User Booking
- `POST /api/v1/bookings`
- `GET /api/v1/bookings/my`
- `GET /api/v1/bookings/{booking_id}`
- `POST /api/v1/bookings/{booking_id}/cancel`

## 11.4 Payment
- `POST /api/v1/payments/create-intent`
- `POST /api/v1/payments/webhook/{provider}`
- `GET /api/v1/payments/{booking_id}/status`

## 11.5 Admin
- Hostel CRUD: `/api/v1/admin/hostels`
- Room CRUD: `/api/v1/admin/rooms`
- Booking review: `/api/v1/admin/bookings/{id}/approve|reject`
- Check-in/out: `/api/v1/admin/bookings/{id}/checkin|checkout`
- Availability block: `/api/v1/admin/availability/blocks`
- Payment list/reconcile/refund: `/api/v1/admin/payments`
- Analytics summary: `/api/v1/admin/analytics/summary`

---

## 12. Payment Integration
### Flow
1. Backend creates payment order/intent with provider.
2. Frontend completes payment using provider SDK or hosted checkout.
3. Provider sends webhook callback.
4. Backend verifies signature and idempotency.
5. Payment record updated.
6. Booking status synchronized.

### Webhook/Callback Requirements
- Validate HMAC signature (`X-Signature`).
- Enforce idempotency key (`provider_ref` unique).
- Retry-safe endpoint (same event can arrive multiple times).
- Log raw webhook payload for audit/debug.

### Provider Strategy
- `PaymentProvider` interface:
  - `create_intent()`
  - `verify_webhook()`
  - `fetch_payment_status()`
  - `refund()`
- Implementations:
  - `MockProvider` for local/staging.
  - `StripeProvider` and/or `RazorpayProvider`.

---

## 13. Non-Functional Requirements
### Performance
- P95 API response < 500ms for read endpoints (excluding external payment calls).
- Search endpoints paginated and indexed.

### Reliability
- Payment webhooks are idempotent.
- Critical flows are transaction-protected.

### Observability
- Structured logs with request ID and user ID.
- Error monitoring (Sentry/OpenTelemetry optional).

---

## 14. Security Considerations
- Password hashing with `bcrypt` or `argon2`.
- JWT best practices:
  - Short-lived access tokens.
  - Refresh token rotation + revocation.
  - Secret/key rotation policy.
- API protection:
  - RBAC middleware.
  - Rate limiting on auth/search/payment endpoints.
  - CSRF protection for cookie-based refresh flows.
- Input validation + output encoding.
- SQL injection prevention via ORM/parameterized queries.
- Secure headers (`HSTS`, `X-Frame-Options`, `CSP` baseline).
- Audit logging for admin actions and booking/payment state changes.

---

## 15. Scalability Considerations
- Modular Flask blueprint architecture for independent services/modules.
- DB indexing strategy for search and booking validation.
- Read-heavy optimizations:
  - Optional Redis caching for hostel listing/search queries.
  - CDN for hostel images.
- Async job queue (Celery/RQ optional) for emails, webhook retries, reports.
- Horizontal scaling readiness:
  - Stateless backend with externalized session/token storage strategy.

---

## 16. Deployment Architecture

## 16.1 Backend Deployment (PythonAnywhere)
### Steps
1. Create PythonAnywhere web app for Flask.
2. Configure virtualenv and install dependencies.
3. Set WSGI file to load Flask app factory.
4. Configure environment variables in PythonAnywhere (via web app config or `.env` loaded securely).
5. Connect to PostgreSQL (managed DB; SSL enabled if external).
6. Run migrations (`Flask-Migrate`/Alembic).
7. Configure static/media handling (hostel images via object storage recommended).
8. Set HTTPS and allowed hosts/CORS.

### Required Environment Variables (Backend)
- `FLASK_ENV`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `FRONTEND_URL`
- `MAIL_*` vars for reset emails
- `PAYMENT_PROVIDER`
- `STRIPE_SECRET_KEY` / `RAZORPAY_KEY_SECRET`
- `WEBHOOK_SECRET`

### WSGI Notes
- Point to app object: `from app import create_app; application = create_app()`
- Enable log files for request/error tracing.

## 16.2 Frontend Deployment (Vercel)
### Steps
1. Connect repo to Vercel project.
2. Build command defaults for Next.js App Router.
3. Set environment variables per environment.
4. Configure API base URL to PythonAnywhere backend.
5. Deploy preview and production branches.
6. Verify rewrites/headers and CORS with backend domain.

### Required Environment Variables (Frontend)
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_PAYMENT_PROVIDER_KEY` (publishable key only)
- `NEXT_PUBLIC_APP_ENV`

### API Integration
- Use server actions/route handlers where needed for secure token handling.
- Centralized API client with automatic token refresh and 401 retry strategy.

---

## 17. Testing Plan
### Unit Tests
- Auth services (password hash/verify, token generation, reset token logic).
- Booking validator (date overlap, state transitions).
- Payment adapter logic (intent creation, webhook signature verification).

### API Tests
- Endpoint contract tests (`pytest` + `requests`/`httpx` + Flask test client).
- RBAC tests for guest/user/admin access boundaries.
- Error path tests (invalid dates, payment failure, duplicate webhook).

### End-to-End Tests
- User journey:
  - Register -> login -> search -> booking -> payment -> confirmation.
- Admin journey:
  - Add hostel/room -> approve booking -> check-in/out -> analytics view.
- Tooling: Playwright/Cypress for frontend + mocked payment where needed.

### Regression & Release Gates
- Must-pass checks before production deploy:
  - Unit + API tests.
  - Critical E2E smoke tests.
  - Migration validation on staging DB snapshot.

---

## 18. Milestones (Suggested)
1. Foundation (Week 1-2): Auth, DB schema, base Next.js app, Flask skeleton.
2. Core Booking (Week 3-4): Hostel/room CRUD, search, booking engine.
3. Admin Ops (Week 5): Approval, availability block, check-in/out.
4. Payments (Week 6): Mock + Stripe/Razorpay adapter and webhook sync.
5. Hardening (Week 7): Security, tests, analytics, deployment readiness.
6. Go-Live (Week 8): Production deploy to PythonAnywhere + Vercel, smoke tests.

---

## 19. Risks and Mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| Payment webhook delays/failures | Booking/payment mismatch | Idempotent retries + reconcile endpoint + admin manual reconcile |
| Race conditions in booking | Double booking | Transaction + locking + overlap constraint |
| Poor search performance at scale | User drop-off | Proper indexes + pagination + optional Redis cache |
| Admin misuse/errors | Data inconsistency | Audit logs + role scoping + validation constraints |
| Deployment config drift | Outages | Environment parity checklist + staging smoke tests |

---

## 20. Definition of Done
- All in-scope features implemented and validated.
- No critical or high-severity open defects.
- Security baseline controls enabled.
- Monitoring/logging active for key flows.
- Production deployment complete on:
  - Backend: PythonAnywhere
  - Frontend: Vercel
- Runbook and handover docs delivered.

---

## Appendix A: Booking State Transition Rules (Reference)
| From | To | Allowed By |
|---|---|---|
| `draft` | `pending_admin_approval` | user |
| `pending_admin_approval` | `awaiting_payment` | admin |
| `pending_admin_approval` | `rejected` | admin |
| `awaiting_payment` | `payment_pending` | system/user |
| `payment_pending` | `confirmed` | system (webhook success) |
| `payment_pending` | `failed/cancelled` | system/user |
| `confirmed` | `checked_in` | admin |
| `checked_in` | `checked_out` | admin |
| `checked_out` | `completed` | system/admin |
| `confirmed` | `cancelled` | user/admin (policy-based) |

## Appendix B: Suggested Folder Structure (Reference)
```text
backend/
  app/
    api/v1/
      auth.py
      users.py
      hostels.py
      bookings.py
      payments.py
      admin.py
    models/
    services/
    repositories/
    middleware/
    config/
  migrations/
  tests/

frontend/
  app/
    (public)/
    (auth)/
    dashboard/
    hostels/
    booking/
    payment/
    profile/
    admin/
  components/
  lib/
  tests/
```
