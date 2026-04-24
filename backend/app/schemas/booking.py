from marshmallow import Schema, fields, validate, validates_schema, ValidationError, RAISE

BOOKING_STATUSES = [
    "draft",
    "pending_admin_approval",
    "awaiting_payment",
    "payment_pending",
    "confirmed",
    "checked_in",
    "checked_out",
    "completed",
    "rejected",
    "cancelled",
    "expired",
]


class BookingCreateSchema(Schema):
    class Meta:
        unknown = RAISE

    hostel_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    check_in = fields.Date(required=True)
    check_out = fields.Date(required=True)
    guests_count = fields.Int(required=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_dates(self, data, **kwargs):
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        if check_in is not None and check_out is not None:
            if check_out <= check_in:
                raise ValidationError(
                    "check_out must be after check_in.",
                    field_name="check_out",
                )


class BookingOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    hostel_id = fields.Int(dump_only=True)
    room_id = fields.Int(dump_only=True)
    check_in = fields.Date(dump_only=True)
    check_out = fields.Date(dump_only=True)
    guests_count = fields.Int(dump_only=True)
    nights_count = fields.Int(dump_only=True)
    total_amount = fields.Decimal(dump_only=True, as_string=True, places=2)
    status = fields.Str(dump_only=True)
    admin_notes = fields.Str(dump_only=True, allow_none=True)
    hold_expires_at = fields.DateTime(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BookingActionSchema(Schema):
    class Meta:
        unknown = RAISE

    admin_notes = fields.Str(load_default=None, validate=validate.Length(max=500))


class BookingListQuerySchema(Schema):
    class Meta:
        unknown = RAISE

    status = fields.Str(
        load_default=None,
        validate=validate.OneOf(BOOKING_STATUSES),
    )
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=50))


class AdminBookingListQuerySchema(Schema):
    class Meta:
        unknown = RAISE

    status = fields.Str(
        load_default=None,
        validate=validate.OneOf(BOOKING_STATUSES),
    )
    hostel_id = fields.Int(load_default=None)
    user_id = fields.Int(load_default=None)
    date_from = fields.Date(load_default=None)
    date_to = fields.Date(load_default=None)
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=50))
