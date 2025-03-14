from datetime import datetime

from marshmallow import Schema, fields, ValidationError, validates, validate

from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates, validate


class PaymentAddSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(
        min=0.01, error="El monto debe ser mayor que 0.01"))
    # Accepts date in 'MM/DD/YYYY' format
    date = fields.Date(required=True, format='%d/%m/%Y')
    member_id = fields.Int(required=False,
                           validate=validate.Range(min=1, error="El ID del miembro debe ser un número entero positivo"))
    type = fields.Str(required=True, validate=validate.OneOf(["Honorarios", "Proveedor", "Gastos Varios"],
                                                             error="El tipo de pago debe ser 'Honorarios', 'Proveedor' o 'Gastos Varios'"))
    description = fields.Str(required=False,
                             validate=validate.Length(max=255,
                                                      error="La descripción debe tener menos de 255 caracteres"))

    @validates('date')
    def validate_payment_date(self, value):
        """
                Validate that the payment date is not in the future.

                Args:
                    value (datetime.date): The payment date to validate.

                Raises:
                    ValidationError: If the payment date is in the future.
        """
        if value > datetime.today().date():
            raise ValidationError(
                "La fecha de pago no puede estar en el futuro.")
