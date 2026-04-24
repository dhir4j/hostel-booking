from marshmallow import Schema, fields, validate, validates_schema, ValidationError, RAISE


class AmenitySchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class HostelImageSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    hostel_id = fields.Int(dump_only=True)
    image_url = fields.Str(dump_only=True)
    is_primary = fields.Bool(dump_only=True)
    sort_order = fields.Int(dump_only=True)


class HostelOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True, allow_none=True)
    city = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    latitude = fields.Decimal(dump_only=True, as_string=True, allow_none=True)
    longitude = fields.Decimal(dump_only=True, as_string=True, allow_none=True)
    status = fields.Str(dump_only=True)
    auto_approve = fields.Bool(dump_only=True)
    amenities = fields.List(fields.Nested(AmenitySchema), dump_only=True)
    images = fields.List(fields.Nested(HostelImageSchema), dump_only=True)
    price_from = fields.Decimal(dump_only=True, as_string=True, places=2, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class HostelSummarySchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    city = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    cover_image_url = fields.Str(dump_only=True, allow_none=True)
    amenities = fields.List(fields.Str(), dump_only=True)
    price_from = fields.Decimal(dump_only=True, as_string=True, places=2, allow_none=True)


class HostelCreateSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default=None)
    city = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=300))
    latitude = fields.Decimal(load_default=None, as_string=True)
    longitude = fields.Decimal(load_default=None, as_string=True)
    status = fields.Str(
        load_default="active",
        validate=validate.OneOf(["active", "inactive", "pending"]),
    )
    auto_approve = fields.Bool(load_default=False)
    amenity_ids = fields.List(fields.Int(), load_default=list)
    image_urls = fields.List(fields.Str(), load_default=list)


class HostelUpdateSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    city = fields.Str(validate=validate.Length(min=1, max=100))
    address = fields.Str(validate=validate.Length(min=1, max=300))
    latitude = fields.Decimal(as_string=True, allow_none=True)
    longitude = fields.Decimal(as_string=True, allow_none=True)
    status = fields.Str(validate=validate.OneOf(["active", "inactive", "pending"]))
    auto_approve = fields.Bool()
    amenity_ids = fields.List(fields.Int())
    image_urls = fields.List(fields.Str())


class HostelListQuerySchema(Schema):
    class Meta:
        unknown = RAISE

    city = fields.Str(load_default=None)
    min_price = fields.Decimal(load_default=None, as_string=True, places=2)
    max_price = fields.Decimal(load_default=None, as_string=True, places=2)
    check_in = fields.Date(load_default=None)
    check_out = fields.Date(load_default=None)
    guests = fields.Int(load_default=None, validate=validate.Range(min=1))
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=50))
    sort = fields.Str(
        load_default=None,
        validate=validate.OneOf(["price_asc", "price_desc", "name"]),
    )

    @validates_schema
    def validate_dates(self, data, **kwargs):
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        if check_in is not None:
            if check_out is None:
                raise ValidationError(
                    "check_out is required when check_in is provided.",
                    field_name="check_out",
                )
            if check_out <= check_in:
                raise ValidationError(
                    "check_out must be after check_in.",
                    field_name="check_out",
                )
