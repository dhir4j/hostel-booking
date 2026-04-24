from marshmallow import Schema, fields, validate, RAISE


class PaymentIntentRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    booking_id = fields.Int(required=True)


class PaymentIntentResponseSchema(Schema):
    class Meta:
        unknown = RAISE

    provider = fields.Str(dump_only=True)
    provider_ref = fields.Str(dump_only=True)
    amount = fields.Decimal(dump_only=True, as_string=True, places=2)
    currency = fields.Str(dump_only=True)
    client_secret = fields.Str(dump_only=True, allow_none=True)


class PaymentOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    booking_id = fields.Int(dump_only=True)
    provider = fields.Str(dump_only=True)
    provider_ref = fields.Str(dump_only=True, allow_none=True)
    amount = fields.Decimal(dump_only=True, as_string=True, places=2)
    currency = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    failure_reason = fields.Str(dump_only=True, allow_none=True)
    paid_at = fields.DateTime(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class PaymentStatusSchema(Schema):
    class Meta:
        unknown = RAISE

    booking_id = fields.Int(dump_only=True)
    booking_status = fields.Str(dump_only=True)
    payment_status = fields.Str(dump_only=True, allow_none=True)
    last_payment = fields.Nested(PaymentOutSchema, dump_only=True, allow_none=True)


class PaymentRefundSchema(Schema):
    class Meta:
        unknown = RAISE

    reason = fields.Str(load_default=None)


class AdminPaymentListQuerySchema(Schema):
    class Meta:
        unknown = RAISE

    status = fields.Str(load_default=None)
    date_from = fields.Date(load_default=None)
    date_to = fields.Date(load_default=None)
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=50))
