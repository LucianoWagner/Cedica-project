from marshmallow import Schema, fields, ValidationError, validates, validate
import bleach


class UserAddSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(
        error="El email no es válido"))
    alias = fields.Str(required=True,
                       validate=validate.Length(max=100, error="El alias debe ser menor de 100 caracteres"))
    password = fields.Str(required=True,
                          validate=validate.Length(min=6, error="La contraseña debe tener al menos 6 caracteres"))
    role_id = fields.Int(required=True)
    member_id = fields.Int(required=True)

    @validates('alias')
    def validate_and_sanitize_alias(self, value):
        sanitized_value = bleach.clean(value, strip=True)
        if sanitized_value != value:
            raise ValidationError(
                "El alias contiene caracteres no permitidos.")
        return sanitized_value

    @validates('password')
    def validate_and_sanitize_password(self, value):
        sanitized_value = bleach.clean(value, strip=True)
        if sanitized_value != value:
            raise ValidationError(
                "La contraseña contiene caracteres no permitidos.")
        return sanitized_value


class UserEditSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(
        error="El email no es válido"))
    alias = fields.Str(required=True,
                       validate=validate.Length(max=100, error="El alias debe ser menor de 100 caracteres"))
    change_password = fields.Bool(required=True)
    password = fields.Str(required=False,
                          validate=validate.Length(min=6, error="La contraseña debe tener al menos 6 caracteres"))
    role_id = fields.Int(required=True)
    active = fields.Bool(required=True)

    def validate(self, data, **kwargs):
        """
                Validate the user edit data.

                Args:
                    data (dict): The data to validate.
                    **kwargs: Additional keyword arguments.

                Returns:
                    dict: The validated data.

                Raises:
                    ValidationError: If validation fails.
        """
        errors = {}

        # Validate change_password and password
        change_password = data.get('change_password')
        password = data.get('password')

        if change_password:
            if not password:
                errors['password'] = [
                    "La contraseña es requerida si se cambia la contraseña."]
        else:
            if password:
                errors['password'] = [
                    "La contraseña no debe ser proporcionada si no se cambia."]

        if errors:
            raise ValidationError(errors)

        return data


class UserApprovalSchema(Schema):
    role_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
