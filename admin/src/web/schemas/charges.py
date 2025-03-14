from marshmallow import Schema, fields, validate


class CobroAddSchema(Schema):
    date = fields.Date(required=True, format='%d/%m/%Y')
    payment_method = fields.Str(required=True, validate=validate.OneOf(
        ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito",
            "Transferencia Bancaria", "Otro"],
        error="El medio de pago debe ser 'Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia Bancaria' o 'Otro'"))
    jya_id = fields.Int(required=False,
                        validate=validate.Range(min=1, error="El ID de la JYA debe ser un número entero positivo"))
    member_id = fields.Int(required=False,
                           validate=validate.Range(min=1, error="El ID del miembro debe ser un número entero positivo"))
    amount = fields.Float(required=True, validate=validate.Range(
        min=0.01, error="El monto debe ser mayor que 0.01"))
    observations = fields.Str(required=False, validate=validate.Length(max=255,
                                                                       error="Las observaciones deben tener menos 255 caracteres"))
