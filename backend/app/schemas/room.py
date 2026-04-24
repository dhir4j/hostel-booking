from marshmallow import Schema, fields, validate, validates_schema, ValidationError, RAISE

_AVAILABILITY_STATUSES = ["available", "occupied", "maintenance", "blocked"]


class RoomOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    hostel_id = fields.Int(dump_only=True)
    room_number = fields.Str(dump_only=True)
    room_type = fields.Str(dump_only=True, allow_none=True)
    capacity = fields.Int(dump_only=True)
    price_per_night = fields.Decimal(dump_only=True, as_string=True, places=2)
    availability_status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class RoomCreateSchema(Schema):
    class Meta:
        unknown = RAISE

    hostel_id = fields.Int(required=True)
    room_number = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    room_type = fields.Str(load_default=None)
    capacity = fields.Int(required=True, validate=validate.Range(min=1))
    price_per_night = fields.Decimal(required=True, as_string=True, places=2)
    availability_status = fields.Str(
        load_default="available",
        validate=validate.OneOf(_AVAILABILITY_STATUSES),
    )


class RoomUpdateSchema(Schema):
    class Meta:
        unknown = RAISE

    room_number = fields.Str(validate=validate.Length(min=1, max=30))
    room_type = fields.Str(allow_none=True)
    capacity = fields.Int(validate=validate.Range(min=1))
    price_per_night = fields.Decimal(as_string=True, places=2)
    availability_status = fields.Str(validate=validate.OneOf(_AVAILABILITY_STATUSES))


class RoomBlockOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    room_id = fields.Int(dump_only=True)
    start_date = fields.Date(dump_only=True)
    end_date = fields.Date(dump_only=True)
    reason = fields.Str(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class RoomBlockCreateSchema(Schema):
    class Meta:
        unknown = RAISE

    room_id = fields.Int(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    reason = fields.Str(required=True, validate=validate.Length(min=1, max=200))

    @validates_schema
    def validate_dates(self, data, **kwargs):
        start = data.get("start_date")
        end = data.get("end_date")
        if start is not None and end is not None:
            if end <= start:
                raise ValidationError(
                    "end_date must be after start_date.",
                    field_name="end_date",
                )
