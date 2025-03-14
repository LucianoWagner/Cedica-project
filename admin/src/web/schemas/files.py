from marshmallow import fields, Schema
from marshmallow.validate import Length


class FileSchema(Schema):
    file_name = fields.String(required=True, validate=Length(min=1))
    file_type = fields.String(required=True, validate=Length(min=1))
    file_id = fields.String(required=True)
    # We are just validating here, actual file is handled in the controller.
    content_type = fields.String(required=True)
    content_length = fields.Integer(required=True)


class LinkSchema(Schema):
    link_name = fields.String(required=True, validate=Length(min=1))
    link_type = fields.String(required=True, validate=Length(min=1))
    # Validates the URL format
    link_url = fields.String(required=True, validate=Length(min=1))
