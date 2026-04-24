from marshmallow import Schema, fields, validate, validates_schema, ValidationError, RAISE


class RegisterSchema(Schema):
    class Meta:
        unknown = RAISE

    full_name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None, validate=validate.Length(max=30))
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )


class LoginSchema(Schema):
    class Meta:
        unknown = RAISE

    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class ForgotPasswordSchema(Schema):
    class Meta:
        unknown = RAISE

    email = fields.Email(required=True)


class ResetPasswordSchema(Schema):
    class Meta:
        unknown = RAISE

    token = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )


class ChangePasswordSchema(Schema):
    class Meta:
        unknown = RAISE

    current_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )


class TokenResponseSchema(Schema):
    class Meta:
        unknown = RAISE

    access_token = fields.Str(dump_only=True)
