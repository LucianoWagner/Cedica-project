from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

from marshmallow import Schema, fields, validate, ValidationError, validates, post_load, validates_schema

from core.people import Member, Person
from web.schemas.files import FileSchema, LinkSchema


class PersonSchema(Schema):
    name = fields.Str(required=True,
                      validate=validate.Length(max=255, error="El nombre debe tener menos de 255 caracteres"))
    surname = fields.Str(required=True,
                         validate=validate.Length(max=255, error="El apellido debe tener menos de 255 caracteres"))
    dni = fields.Int(required=True, validate=validate.Range(
        min=1, error="El DNI debe ser un número entero positivo"))
    address = fields.Str(required=True,
                         validate=validate.Length(max=255, error="La dirección debe tener menos de 255 caracteres"))
    telephone = fields.Str(required=True,
                           validate=validate.Length(max=255, error="El teléfono debe tener menos de 255 caracteres"))
    emergency_contact = fields.Str(required=True, validate=validate.Length(max=255,
                                                                           error="El contacto de emergencia debe tener menos de 255 caracteres"))


class MemberAddSchema(Schema):
    email = fields.Email(required=True, error_messages={
                         "required": "El correo electrónico es obligatorio"})
    locality = fields.Str(required=True,
                          validate=validate.Length(max=255, error="La localidad debe tener menos de 255 caracteres"))
    profession = fields.Str(required=True,
                            validate=validate.Length(max=255, error="La profesión debe tener menos de 255 caracteres"))
    job_position = fields.Str(required=True, validate=validate.Length(max=255,
                                                                      error="El puesto de trabajo debe tener menos de 255 caracteres"))
    start_date = fields.Date(required=True, format='%d/%m/%Y',
                             error_messages={"required": "La fecha de inicio es obligatoria"})
    end_date = fields.Date(format='%d/%m/%Y')
    medical_insurance = fields.Str(required=True, validate=validate.Length(max=255,
                                                                           error="El seguro médico debe tener menos de 255 caracteres"))
    insurance_number = fields.Str(required=True, validate=validate.Length(max=255,
                                                                          error="El número de seguro debe tener menos de 255 caracteres"))
    job_condition = fields.Str(required=True, validate=validate.Length(max=255,
                                                                       error="La condición laboral debe tener menos de 255 caracteres"))
    active = fields.Bool(required=True, error_messages={
                         "required": "El estado activo es obligatorio"})
    person = fields.Nested(PersonSchema, required=True)

    start_date = fields.Date(required=True, format='%d/%m/%Y',
                             error_messages={"required": "La fecha de inicio es obligatoria"})
    end_date = fields.Date(format='%d/%m/%Y')

    files = fields.List(fields.Nested(FileSchema), required=True)
    links = fields.List(fields.Nested(LinkSchema), required=False)

    @validates('end_date')
    def validate_end_date(self, value):
        """
               Validate that the end date is not earlier than the start date.

               Args:
                   value (datetime.date): The end date to validate.

               Raises:
                   ValidationError: If the end date is earlier than the start date.
        """
        start_date_str = self.context.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
        else:
            start_date = None

        if value and start_date and value < start_date:
            raise ValidationError(
                "La fecha de finalización no puede ser anterior a la fecha de inicio.")

    # Post load remains unchanged
    @post_load
    def make_member(self, data, **kwargs):
        """
                Create a Member instance from the validated data.

                Args:
                    data (dict): The validated data.

                Returns:
                    dict: The data with a Person instance.
        """
        person_data = data.pop('person')
        person = Person(**person_data)
        return {**data, "person": person}


def validate_date_format(value):
    """
        Validate that the date is in the correct format.

        Args:
            value (str): The date string to validate.

        Returns:
            datetime: The parsed datetime object.

        Raises:
            ValidationError: If the date format is invalid.
    """
    try:
        return datetime.strptime(value, '%d/%m/%Y')
    except ValueError:
        raise ValidationError('Invalid date format. Should be dd/mm/yyyy.')


def validate_start_end_dates(data):
    """
        Validate that the start date is not later than the end date.

        Args:
            data (dict): The data containing start and end dates.

        Raises:
            ValidationError: If the start date is later than the end date.
    """
    start_date = datetime.strptime(data['start_date'], '%d/%m/%Y')
    end_date = datetime.strptime(
        data['end_date'], '%d/%m/%Y') if data.get('end_date') else None
    if end_date and start_date > end_date:
        raise ValidationError('start_date cannot be older than end_date.')


class MemberEditSchema(Schema):
    id = fields.Int(dump_only=True)
    person_id = fields.Int(required=True)
    email = fields.Str(required=True, validate=validate.Email())
    locality = fields.Str(required=True)
    profession = fields.Str(required=True)
    job_position = fields.Str(required=True)
    start_date = fields.Str(required=True, validate=validate_date_format)
    end_date = fields.Str(validate=validate_date_format, allow_none=True)
    medical_insurance = fields.Str(required=True)
    insurance_number = fields.Str(required=True)
    job_condition = fields.Str(required=True)
    active = fields.Bool(required=True)

    files = fields.List(fields.Nested(FileSchema), required=True)
    links = fields.List(fields.Nested(LinkSchema), required=False)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        """
                Validate that the start and end dates are in the correct order.

                Args:
                    data (dict): The data containing start and end dates.

                Raises:
                    ValidationError: If the start date is later than the end date.
        """
        if data.get('start_date') and data.get('end_date'):
            validate_start_end_dates(data)
