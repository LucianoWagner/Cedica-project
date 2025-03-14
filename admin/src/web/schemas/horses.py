from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Email, OneOf
import datetime

from werkzeug.datastructures import FileStorage

from web.schemas.files import FileSchema, LinkSchema


class HorseAddSchema(Schema):
    name = fields.String(required=True, validate=Length(min=1, max=100))
    birth_date = fields.Date(required=True, format='%d/%m/%Y')
    sex = fields.String(required=True, validate=OneOf(
        ["Masculino", "Femenino"]))
    race = fields.String(required=True, validate=Length(min=1, max=50))
    fur = fields.String(required=True, validate=Length(min=1, max=50))
    origin = fields.String(required=True, validate=Length(min=1, max=100))
    entry_date = fields.Date(required=True, format='%d/%m/%Y')
    headquarter = fields.String(required=True, validate=Length(min=1, max=100))
    jya_type = fields.String(required=True, validate=Length(min=1, max=50))
    riders = fields.List(fields.String(), required=True,
                         validate=Length(min=1))
    trainers = fields.List(
        fields.String(), required=True, validate=Length(min=1))

    # Nested schema for files
    files = fields.List(fields.Nested(FileSchema), required=True)

    # Nested schema for links
    links = fields.List(fields.Nested(LinkSchema), required=False)

    @validates('birth_date')
    def validate_birth_date(self, value):
        """Ensure birth date is not in the future."""
        if value > datetime.date.today():
            raise ValidationError("Birth date cannot be in the future.")

    @validates('entry_date')
    def validate_entry_date(self, value):
        """Ensure entry date is not in the future."""
        if value > datetime.date.today():
            raise ValidationError("Entry date cannot be in the future.")
