from marshmallow import Schema, fields, validate, pre_load

from web.schemas.files import FileSchema, LinkSchema
from web.schemas.members import PersonSchema


class JyAAddSchema(Schema):
    person = fields.Nested(PersonSchema, required=True)
    age = fields.Int(required=True, validate=validate.Range(
        min=0, error="The age must be a positive number"))
    birth_date = fields.Date(required=True, format='%d/%m/%Y')
    birth_place = fields.Str(required=True,
                             validate=validate.Length(max=255, error="The birthplace must be less than 255 characters"))

    granted = fields.Bool(required=True)
    grant_percentage = fields.Float(required=False, validate=validate.Range(min=0, max=100,
                                                                            error="The scholarship percentage must be between 0 and 100"))
    professionals = fields.List(fields.Int(), required=False)
    behind_payment = fields.Bool(required=False)
    files = fields.List(fields.Nested(FileSchema), required=True)
    links = fields.List(fields.Nested(LinkSchema), required=False)

    # @pre_load
    # def process_input(self, data, **kwargs):
    #     # Convert string fields to appropriate types
    #     if 'age' in data:
    #         data['age'] = int(data['age'])
    #     if 'scholarship_percentage' in data:
    #         data['scholarship_percentage'] = float(data['scholarship_percentage'])
    #     if 'behind_payment' in data:
    #         data['behind_payment'] = data['behind_payment'].lower() == 'true'
    #     if 'professionals' in data:
    #         if isinstance(data['professionals'], str):
    #             data['professionals'] = [int(data['professionals'])]
    #         else:
    #             data['professionals'] = [int(prof) for prof in data['professionals']]
    #     return data
