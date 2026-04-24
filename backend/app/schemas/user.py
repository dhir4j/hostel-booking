from marshmallow import Schema, fields, validate, RAISE


class UserOutSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Int(dump_only=True)
    full_name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    phone = fields.Str(dump_only=True, allow_none=True)
    role = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(Schema):
    class Meta:
        unknown = RAISE

    full_name = fields.Str(validate=validate.Length(min=1, max=120))
    phone = fields.Str(validate=validate.Length(max=30), allow_none=True)
