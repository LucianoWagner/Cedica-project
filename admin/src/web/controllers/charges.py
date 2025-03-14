from flask import render_template, session, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from web.handlers.auth import is_authenticated, login_required, permission_required
from datetime import datetime

from flask import render_template, session, abort, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from core.auth import delete_user
from core.database import db
from core.finance import get_charges, get_charges_quantity, delete_charge, find_charge_by_id, create_charge
from core.people import get_all_members, find_member_by_id, find_jya_by_id, get_all_jyas
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.handlers.pagination import get_total_pages, generate_pagination, paginate
from web.schemas.charges import CobroAddSchema
from web.schemas.payments import PaymentAddSchema
from web.templates.payments import create_payment

charges_blueprint = Blueprint("charges", __name__, url_prefix="/charges")


@charges_blueprint.route("/")
class ChargesResource(MethodView):
    """
        Recurso para gestionar los cobros.

        Métodos:
            get: Muestra una lista de cobros paginada y filtrada.
            post: Crea un nuevo cobro.
        """

    @permission_required("charge_index")
    def get(self):
        """
                Obtiene y renderiza la página con la lista de cobros paginada y con filtros aplicados.

                Se permite ordenar por fecha, filtrar por rango de fechas, metodo de pago, nombre y apellido del miembro.

                Returns:
                    Response: Renderiza la página con los cobros.
                """
        page = request.args.get("page", 1, type=int)
        sort_by = request.args.get("sort_by", "date", type=str)
        order = request.args.get("order", "desc", type=str)
        start_date = request.args.get("start_date", None, type=str)
        end_date = request.args.get("end_date", None, type=str)
        payment_method = request.args.get("payment_method", None, type=str)
        member_name = request.args.get("member_name", None, type=str)
        member_surname = request.args.get("member_surname", None, type=str)
        if start_date:
            start_date = datetime.strptime(
                start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(
                end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        per_page = 10

        charges_data = paginate(lambda **kwargs: get_charges(**kwargs),
                                lambda **kwargs: get_charges_quantity(
                                    **kwargs), sort_by, order, page,
                                start_date=start_date, end_date=end_date, payment_method=payment_method,
                                member_name=member_name, member_surname=member_surname)

        payment_method2 = ["Efectivo", "Transferencia-Bancaria",
                           "Tarjeta-Credito", "Tarjeta-Debito", "Otro"]

        columns = [
            {"name": "jya", "label": "JYA", "sortable": False},
            {"name": "date", "label": "Fecha de pago", "sortable": True},
            {"name": "payment_method", "label": "Metodo de pago", "sortable": False},
            {"name": "amount", "label": "Monto", "sortable": False},
            {"name": "member_name", "label": "Nombre de Miembro", "sortable": False},
            {"name": "nember_surname", "label": "Apellido de Miembro", "sortable": False},
            {"name": "observations", "label": "Observaciones", "sortable": False},
            {"name": "behind_payment", "label": "deuda", "sortable": False}
        ]

        members = get_all_members()
        jyas = get_all_jyas()

        return render_template("charges/charges.html", data=charges_data['items'], count=charges_data['count'],
                               sort_by=sort_by, order=order, per_page=per_page, page=page,
                               total_pages=charges_data['total_pages'], pagination=charges_data['pagination'],
                               columns=columns, members=members, jyas=jyas, payment_method2=payment_method2)

    @permission_required("charge_create")
    def post(self):
        """
                Crea un nuevo cobro a partir de los datos enviados en el formulario.

                Valida los datos del formulario y verifica la existencia de los miembros o JYAs antes de crear el cobro.

                Returns:
                    Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        form_data = request.form.to_dict()  # Recibe datos
        print(form_data)

        schema = CobroAddSchema()
        try:
            validated_data = schema.load(form_data)

            # Verificar si el miembro existe
            if validated_data.get("member_id"):
                member = find_member_by_id(validated_data["member_id"])
                if not member:
                    return jsonify({"message": "El miembro no existe"}), 400
            else:
                validated_data["member_id"] = None

            # verificar si el jya existe
            if validated_data.get("jya_id"):
                jya = find_jya_by_id(validated_data["jya_id"])
                if not jya:
                    return jsonify({"message": "La JYA no existe"}), 400
            else:
                validated_data["jya_id"] = None

            # Crear el registro de cobro
            create_charge(**validated_data)
            return jsonify({"message": "Cobro registrado con éxito"}), 201
        except ValidationError as err:
            return jsonify({"message": err.messages}), 400

    @charges_blueprint.route("/<int:charge_id>", methods=["GET", "PUT", "DELETE"])
    class ChargeResource(MethodView):
        """
            Recurso para gestionar un cobro específico.

            Métodos:
                get: Muestra los detalles de un cobro específico.
                put: Actualiza los datos de un cobro específico.
                delete: Elimina un cobro específico.
        """

        @permission_required("charge_show")
        def get(self, charge_id):
            """
                    Obtiene los detalles de un cobro específico.

                    Returns:
                        Response: Devuelve los datos del cobro en formato JSON o un mensaje de error si no se encuentra.
            """
            charge = find_charge_by_id(charge_id)
            if not charge:
                return jsonify({"message": "El cobro no existe"}), 404

            charge_data = {
                "jya": charge.jya_id,
                "jya_name": charge.jya.person.name,
                "date": charge.date.strftime("%Y-%m-%d"),
                "payment_method": charge.payment_method,
                "amount": charge.amount,
                "member": charge.member_id,
                "member_name": charge.member.person.name,
                "observations": charge.observations,
            }
            return jsonify(charge_data), 200

        @permission_required("charge_update")
        def put(self, charge_id):
            """
                    Actualiza los datos de un cobro específico con los datos proporcionados en el formulario.

                    Valida los datos del formulario y verifica la existencia del miembro y la JYA antes de actualizar.

                    Returns:
                        Response: Devuelve un mensaje de éxito o error en formato JSON.
            """
            form_data = request.form.to_dict()
            schema = CobroAddSchema()
            try:
                validated_data = schema.load(form_data)
                existing_charge = find_charge_by_id(charge_id)

                if not existing_charge:
                    return jsonify({"message": "El cobro no existe"}), 404

                jya = find_jya_by_id(validated_data["jya_id"])
                if not jya:
                    return jsonify({"message": "La JYA no existe"}), 400

                member = find_member_by_id(validated_data["member_id"])
                if not member:
                    return jsonify({"message": "El miembro no existe"}), 400

                existing_charge.jya_id = validated_data["jya_id"]
                existing_charge.date = validated_data["date"]
                existing_charge.payment_method = validated_data["payment_method"]
                existing_charge.amount = validated_data["amount"]
                existing_charge.member_id = validated_data["member_id"]
                existing_charge.observations = validated_data["observations"]

                db.session.commit()

                return jsonify({"message": "Cobro actualizado con éxito"}), 200
            except ValidationError as err:
                return jsonify({"message": err.messages}), 400

        @permission_required("charge_destroy")
        def delete(self, charge_id):
            """
                    Elimina un cobro específico.

                    Returns:
                        Response: Devuelve un mensaje de éxito si el cobro fue eliminado o un mensaje de error si no existe.
            """
            if delete_charge(charge_id):
                return jsonify({"message": "Cobro eliminado con éxito"}), 204
            return jsonify({"message": "El cobro no existe"}), 404
