from datetime import datetime

from flask import render_template, session, abort, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from core.auth import delete_user
from core.database import db
from core.finance import get_payments, get_payments_quantity, delete_payment, find_payment_by_id
from core.people import get_all_members, find_member_by_id
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.handlers.pagination import get_total_pages, generate_pagination, paginate
from web.schemas.payments import PaymentAddSchema
from web.templates.payments import create_payment

payments_blueprint = Blueprint("payments", __name__, url_prefix="/payments")


@payments_blueprint.route("/")
class PaymentsResource(MethodView):
    @permission_required("payment_index")
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de pagos.

        Returns:
            Response: Renderiza la plantilla con la lista de pagos y la paginación.
        """
        page = request.args.get("page", 1, type=int)
        sort_by = request.args.get("sort_by", "date", type=str)
        order = request.args.get("order", "desc", type=str)
        type = request.args.get("type", None, type=str)
        start_date = request.args.get("start_date", None, type=str)
        end_date = request.args.get("end_date", None, type=str)

        if start_date:
            start_date = datetime.strptime(
                start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(
                end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        per_page = 10

        payments_data = paginate(lambda **kwargs: get_payments(**kwargs),
                                 lambda **kwargs: get_payments_quantity(**kwargs), sort_by, order, page, type=type,
                                 start_date=start_date, end_date=end_date)

        payment_types = ["Honorarios", "Proveedor", "Gastos Varios"]
        columns = [
            {"name": "date", "label": "Fecha de pago", "sortable": True},
            {"name": "amount", "label": "Monto", "sortable": False},
            {"name": "type", "label": "Tipo", "sortable": False},
            {"name": "description", "label": "Descripcion", "sortable": False},
            {"name": "member", "label": "Miembro", "sortable": False},
            {"name": "created_at", "label": "Fecha de Creacion", "sortable": False}
        ]

        members = get_all_members()

        return render_template("payments/payments.html", data=payments_data['items'], count=payments_data['count'],
                               sort_by=sort_by, order=order, per_page=per_page, page=page,
                               total_pages=payments_data['total_pages'], pagination=payments_data['pagination'],
                               columns=columns, payment_types=payment_types, members=members)

    @permission_required("payment_create")
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo pago.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()
        schema = PaymentAddSchema()
        try:
            validated_data = schema.load(form_data)
            print(validated_data["date"])
            if validated_data.get("member_id"):
                member = find_member_by_id(validated_data["member_id"])
                if not member:
                    abort(400, "El miembro no existe")
            else:
                validated_data["member_id"] = None

            create_payment(**validated_data)
            return jsonify({"message": "Pago creado con exito"}), 201
        except ValidationError as err:
            return jsonify(err.messages), 400

    @permission_required("payments_update")
    def put(self):
        """
        Maneja la solicitud PUT para actualizar un pago existente.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        pass


@payments_blueprint.route("/<int:payment_id>")
class PaymentResource(MethodView):

    @permission_required("payment_update")
    def put(self, payment_id):
        """
        Maneja la solicitud PUT para actualizar un pago específico.

        Args:
            payment_id (int): ID del pago a actualizar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()
        schema = PaymentAddSchema()
        try:
            validated_data = schema.load(form_data)
            existing_payment = find_payment_by_id(payment_id)

            if not existing_payment:
                return jsonify({"error": "El pago no existe"}), 404

            if validated_data["type"] == "Honorarios":
                member = find_member_by_id(validated_data["member_id"])
                if not member:
                    return jsonify({"error": "El miembro no existe"}), 400
                existing_payment.member_id = validated_data["member_id"]
            else:
                existing_payment.member_id = None

            existing_payment.amount = validated_data["amount"]
            existing_payment.date = validated_data["date"]
            existing_payment.type = validated_data["type"]
            existing_payment.description = validated_data["description"]

            db.session.commit()

            return jsonify({"message": "Pago actualizado con exito"}), 200
        except ValidationError as err:
            return jsonify(err.messages), 400

    @permission_required("payment_destroy")
    def delete(self, payment_id):
        """
        Maneja la solicitud DELETE para eliminar un pago específico.

        Args:
            payment_id (int): ID del pago a eliminar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        if delete_payment(payment_id):
            return jsonify({"message": "Pago eliminado con exito"}), 204
        return jsonify({"error": "El pago no existe"}), 404
