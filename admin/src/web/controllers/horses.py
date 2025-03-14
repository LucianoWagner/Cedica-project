import base64
from datetime import datetime
from os import fstat

from flask import render_template, session, abort, request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
import ulid

from core.database import db
from core.files import create_file, upload_files, extract_files_data, extract_link_data, delete_file, update_file_key, \
    generate_ulid, process_edit_files, get_filtered_files_data
from core.horses import get_horses, get_horses_quantity, Horse, create_horse, delete_horse, find_horse_by_id
from core.people import get_all_members, find_member_by_id
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.handlers.pagination import paginate
from web.schemas.horses import HorseAddSchema
from werkzeug.datastructures import FileStorage

horses_blueprint = Blueprint("horses", __name__, url_prefix="/horses")


def extract_horse_data():
    """Extrae los datos del caballo de la solicitud."""
    files_data = extract_files_data()

    return {
        "name": request.form.get("name"),
        "birth_date": request.form.get("birth_date"),
        "sex": request.form.get("sex"),
        "race": request.form.get("race"),
        "fur": request.form.get("fur"),
        "origin": request.form.get("origin"),
        "entry_date": request.form.get("entry_date"),
        "headquarter": request.form.get("headquarter"),
        "jya_type": request.form.get("jya_type"),
        "riders": request.form.getlist("riders"),
        "trainers": request.form.getlist("trainers"),
        "files": files_data,  # Mantener los metadatos del archivo para su procesamiento
        "links": extract_link_data()
    }


@horses_blueprint.route("/")
class HorsesResource(MethodView):
    @permission_required("horse_index")
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de caballos.

        Returns:
            Response: Devuelve una página HTML con la lista de caballos.
        """
        page = request.args.get("page", 1, type=int)
        sort_by = request.args.get("sort_by", "entry_date", type=str)
        order = request.args.get("order", "desc", type=str)
        name = request.args.get("name", None, type=str)
        types = request.args.get("type", None, type=str)

        per_page = 10
        horses_data = paginate(lambda **kwargs: get_horses(**kwargs),
                               lambda **kwargs: get_horses_quantity(**kwargs), sort_by, order, page, name=name,
                               types=types, )

        jya_types = Horse.jya_type.property.columns[0].type.enums

        members = get_all_members()
        today_date = datetime.now().strftime('%d/%m/%Y')
        origins = Horse.origin.property.columns[0].type.enums
        file_types = [
            "Ficha general del caballo",
            "Planificación de Entrenamiento",
            "Informe de Evolución",
            "Carga de Imágenes",
            "Registro veterinario"
        ]
        columns = [
            {"name": "name", "label": "Nombre", "sortable": True},
            {"name": "birth_date", "label": "Fecha de Nacimiento", "sortable": True},
            {"name": "sex", "label": "Sexo", "sortable": False},
            {"name": "race", "label": "Raza", "sortable": False},
            {"name": "fur", "label": "Pelaje", "sortable": False},
            {"name": "origin", "label": "Compra/Donación", "sortable": False},
            {"name": "entry_date", "label": "Fecha de Ingreso", "sortable": True},
            {"name": "headquarter", "label": "Sede Asignada", "sortable": False},
            {"name": "trainers", "label": "Entrenadores", "sortable": False},
            {"name": "riders", "label": "Conductores", "sortable": False},
            {"name": "jya_type", "label": "Tipo de J&A Asignados", "sortable": False}
        ]

        return render_template("horses/horses.html", data=horses_data['items'], count=horses_data['count'],
                               sort_by=sort_by, order=order, page=page, total_pages=horses_data[
                                   'total_pages'],
                               pagination=horses_data['pagination'], columns=columns, per_page=per_page,
                               jya_types=jya_types, origins=origins, members=members, today_date=today_date,
                               file_types=file_types)

    @permission_required("horse_create")
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo caballo.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        try:
            # Extraer datos del caballo sin file_upload para la serialización JSON
            horse_data = extract_horse_data()

            # Preparar datos del caballo para la validación
            schema = HorseAddSchema()
            validated_data = schema.load(
                {key: value for key, value in horse_data.items()})

            client = current_app.storage.client

            files = []
            links = [create_file(link["link_url"], link['link_name'],
                                 link['link_type'], True)
                     for link in validated_data["links"]]

            # Procesar las cargas de archivos directamente
            upload_files(client, validated_data['files'], files)

            riders = [find_member_by_id(rider_id)
                      for rider_id in validated_data["riders"]]
            trainers = [find_member_by_id(trainer_id)
                        for trainer_id in validated_data["trainers"]]
            filtered_data = {key: value for key, value in validated_data.items() if
                             key not in ["files", "links", "trainers", "riders"]}
            new_horse = create_horse(
                files + links, trainers, riders, **filtered_data)

            return jsonify({"message": "El caballo ha sido creado con exito"}), 200

        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@horses_blueprint.route("/<int:horse_id>")
class HorseResource(MethodView):

    def get(self, horse_id):
        """
        Maneja la solicitud GET para obtener los detalles de un caballo específico.

        Returns:
            Response: Devuelve los datos del caballo en formato JSON o un mensaje de error si no se encuentra.
        """
        horse = Horse.query.get(horse_id)
        if horse:
            return jsonify(horse.to_dict()), 200
        return jsonify({"error": "El caballo no existe"}), 404

    @permission_required("horse_update")
    def put(self, horse_id):
        """
        Maneja la solicitud PUT para actualizar los datos de un caballo específico.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        try:
            horse_data = extract_horse_data()
            schema = HorseAddSchema()
            validated_data = schema.load(
                {key: value for key, value in horse_data.items()})
            client = current_app.storage.client

            horse = find_horse_by_id(horse_id)
            if not horse:
                return jsonify({"error": "El caballo no existe"}), 404
            for file in horse.files:
                process_edit_files(file, validated_data, client)

            new_files = []
            new_links = [create_file(link['link_url'], link['link_name'],
                                     link['link_type'], True)
                         for link in validated_data["links"]]
            upload_files(client, validated_data['files'], new_files)
            riders = [find_member_by_id(rider_id)
                      for rider_id in validated_data["riders"]]
            trainers = [find_member_by_id(trainer_id)
                        for trainer_id in validated_data["trainers"]]
            filtered_data = {key: value for key, value in validated_data.items() if
                             key not in ["files", "links", "trainers", "riders"]}
            for key, value in filtered_data.items():
                setattr(horse, key, value)

            horse.files = list(horse.files) + new_files + new_links
            horse.riders = riders
            horse.trainers = trainers
            db.session.commit()

            return jsonify({"message": "Caballo actualizado con exito"}), 200
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        except Exception as e:
            print(e)

            return jsonify({"error": str(e)}), 500

    @permission_required("horse_destroy")
    def delete(self, horse_id):
        """
        Maneja la solicitud DELETE para eliminar un caballo específico.

        Returns:
            Response: Devuelve un mensaje de éxito si el caballo fue eliminado o un mensaje de error si no existe.
        """
        if delete_horse(horse_id):
            return jsonify({"message": "Pago eliminado con exito"}), 204
        return jsonify({"error": "El pago no existe"}), 404


@horses_blueprint.route("/<int:horse_id>/files")
class HorseFilesResource(MethodView):
    def get(self, horse_id):
        """
        Maneja la solicitud GET para obtener los archivos de un caballo específico.

        Returns:
            Response: Devuelve los datos de los archivos en formato JSON o un mensaje de error si no se encuentra.
        """
        title = request.args.get("title", None, type=str)
        type = request.args.get("type", None, type=str)
        print(title, type)
        horse = find_horse_by_id(horse_id)
        if not horse:
            return jsonify({"error": "El caballo no existe"}), 404

        return jsonify(get_filtered_files_data(horse, title=title, type=type)), 200
