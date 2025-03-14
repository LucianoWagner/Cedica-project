from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(
        error="El email no es válido"))
    password = fields.Str(required=True, validate=validate.Length(
        min=6, error="La contraseña debe tener al menos 6 caracteres"))
