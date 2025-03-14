import locale

from flask import request, jsonify, render_template, abort
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.debug import console

from core.database import db
from core.public import Message, get_messages, get_messages_quantity
from web.handlers.auth import login_required, permission_required
from web.handlers.pagination import generate_pagination
import requests
messages_blueprint = Blueprint("messages", __name__, url_prefix="/messages")


# Añade tu clave secreta de reCAPTCHA aquí
RECAPTCHA_SECRET_KEY = '6Le_JIIqAAAAAOh04w5ujjxuiQfyUEKZs25OW3Su'


def verify_recaptcha(token):
    """
    Verifica el token de reCAPTCHA con la API de Google.

    Args:
        token (str): El token de reCAPTCHA enviado desde el cliente.

    Returns:
        bool: True si la verificación es exitosa, False en caso contrario.
    """
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get('success', False)


@messages_blueprint.route("/")
class MessagesResource(MethodView):

    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo mensaje.

        Returns:
            Response: Informa el código de estado.
        """
        try:
            print("entro")
            # Extraer los datos del cuerpo de la solicitud
            data = request.get_json()
            print(data)
            captcha = data.get("captcha")

            if not captcha:
                return jsonify({"error": "El token de reCAPTCHA es obligatorio."}), 400

            if not verify_recaptcha(captcha):
                return jsonify({"error": "La verificación de reCAPTCHA falló."}), 400

            full_name = data.get("full_name")
            email = data.get("email")
            description = data.get("description")

            # Validar campos requeridos
            if not full_name or not email or not description:
                return jsonify({"error": "Faltan campos obligatorios: nombre completo, email, descripcion."}), 400

            # Crear un nuevo mensaje
            new_message = Message(
                full_name=full_name,
                email=email,
                body=description,
                status="Pendiente",  # Estado inicial del mensaje
            )

            # Guardar el mensaje en la base de datos
            db.session.add(new_message)
            db.session.commit()

            # Respuesta de éxito
            return jsonify({"message": "Mensaje creado exitosamente"}), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Se produjo un error al crear el mensaje"}), 500

        except Exception as e:
            return jsonify({"error": "Se produjo un error al crear el mensaje"}), 500

    @login_required
    @permission_required('message_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de mensajes.

        Returns:
            Response: Renderiza la plantilla con la lista de mensajes y la paginación.
        """
        page = request.args.get("page", 1, type=int)
        per_page = 10
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")
        status = request.args.get("status")

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        messages = get_messages(
            page=page, per_page=per_page, sort_by=sort_by, order=order, status=status)

        columns = [
            {"name": "created_at", "label": "Fecha de creación", "sortable": True},
            {"name": "updated_at", "label": "Última actualización", "sortable": True},
            {"name": "full_name", "label": "Nombre completo", "sortable": False},
            {"name": "status", "label": "Estado", "sortable": False},
        ]

        count = get_messages_quantity()
        total_pages = (count + per_page - 1) // per_page
        pagination = generate_pagination(page, total_pages)

        return render_template("messages/messages.html", data=messages.items, pagination=pagination,
                               columns=columns,
                               count=count, total_pages=total_pages,
                               page=page, per_page=per_page,
                               sort_by=sort_by, order=order, status=status)

    @messages_blueprint.route("/<int:message_id>", methods=["GET"])
    @login_required
    @permission_required('message_show')
    def get_message_by_id(message_id):
        """
        Maneja la solicitud GET para obtener los detalles de un mensaje específico.

        Args:
            message_id (int): ID del mensaje a obtener.

        Returns:
            Response: Devuelve los detalles del mensaje en formato JSON.
        """
        message = Message.query.filter_by(id=message_id).first()

        if not message:
            abort(404, description="No se encontró el mensaje")

        return jsonify(message.to_dict())

    @messages_blueprint.route("/<int:message_id>", methods=["PUT"])
    @login_required
    @permission_required('message_update')
    def edit_message(message_id):
        """
        Maneja la solicitud PUT para actualizar un mensaje específico.

        Args:
            message_id (int): ID del mensaje a actualizar.

        Returns:
            Response: Devuelve el resultado de la operación en formato JSON.
        """
        try:
            # Extract form data
            comment = request.form.get('comment')
            status = request.form.get('status')

            VALID_STATUSES = ['Pendiente', 'Contestada']
            # Validate the status value
            if status not in VALID_STATUSES:
                return jsonify({"error": "Estado inválido"}), 400

            # Get message object
            message = Message.query.filter_by(id=message_id).first()

            if not message:
                return jsonify({"error": "Mensaje no encontrado"}), 404

            # Update message object
            message.comment = comment
            message.status = status
            message.updated_at = datetime.utcnow()

            # Commit to database
            db.session.commit()

            return jsonify({"message": "Mensaje actualizado con éxito"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Se produjo un error al actualizar el mensaje"}), 500

        except Exception as e:
            return jsonify({"message": "Se produjo un error al actualizar el mensaje"}), 500

    @messages_blueprint.route("/<int:message_id>", methods=["DELETE"])
    @login_required
    @permission_required('message_destroy')
    def delete_message(message_id):
        """
        Maneja la solicitud DELETE para eliminar un mensaje específico.

        Args:
            message_id (int): ID del mensaje a eliminar.

        Returns:
            Response: Devuelve el resultado de la operación en formato JSON.
        """
        try:
            # Get message object
            message = Message.query.filter_by(id=message_id).first()

            if not message:
                return jsonify({"error": "Mensaje no encontrado"}), 404

            # Delete message object
            db.session.delete(message)
            db.session.commit()

            return jsonify({"message": "Mensaje eliminado con éxito"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Se produjo un error al eliminar el mensaje"}), 500

        except Exception as e:
            return jsonify({"message": "Se produjo un error al eliminar el mensaje"}), 500
