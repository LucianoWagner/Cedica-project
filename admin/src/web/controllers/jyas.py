from datetime import datetime
import locale

from flask import render_template, session, abort, request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from core.database import db
from core.files import extract_files_data, extract_link_data, get_filtered_files_data, delete_file
from core.finance import create_jya_with_person
from core.people import get_jyas_quantity, get_jyas, get_all_members, get_all_professionals, find_member_by_id, \
    create_jya, find_jya_by_id
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.handlers.pagination import generate_pagination, paginate
from web.handlers.validation import validate_schema_with_files
from web.schemas.jya import JyAAddSchema

jyas_blueprint = Blueprint("jyas", __name__, url_prefix="/jyas")


@jyas_blueprint.route("/")
class JyasResource(MethodView):
    @login_required
    @permission_required('jya_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de JYAs.

        Returns:
            Response: Devuelve una página HTML con la lista de JYAs.
        """
        page = request.args.get("page", 1, type=int)
        per_page = 10
        # Orden predeterminado por nombre
        sort_by = request.args.get("sort_by", "name")
        # Orden predeterminado ascendente
        order = request.args.get("order", "asc")
        search = request.args.get("search", None)
        criteria = request.args.get("criteria", None)
        professionals = request.args.get("professional", None)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        jyas_data = paginate(lambda **kwargs: get_jyas(**kwargs), lambda **kwargs: get_jyas_quantity(**kwargs), sort_by,
                             order, page, search=search, criteria=criteria, professionals=professionals)

        columns = [
            {"name": "nombre", "label": "Nombre", "sortable": True},
            {"name": "apellido", "label": "Apellido", "sortable": True},
            {"name": "dni", "label": "DNI", "sortable": False},
            {"name": "telefono", "label": "Teléfono Actual", "sortable": False},
            {"name": "created_at", "label": "Fecha de Creación", "sortable": True}
        ]

        file_types = ["entrevista", "evaluación",
                      "planificaciones", "evolución", "crónicas", "documental"]
        today_date = datetime.now().strftime('%d/%m/%Y')
        all_professionals = get_all_professionals()
        print(all_professionals)

        return render_template("jyas/jyas.html", data=jyas_data['items'], pagination=jyas_data['pagination'],
                               columns=columns,
                               count=jyas_data['count'], total_pages=jyas_data['total_pages'],
                               page=page, per_page=per_page,
                               sort_by=sort_by, order=order,
                               professionals=professionals,
                               all_professionals=all_professionals, file_types=file_types, criteria=criteria,
                               today_date=today_date)

    @permission_required('jya_create')
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo JYA.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        jya_data = extract_jyas_data()
        schema = JyAAddSchema()
        try:
            filtered_data, links, files = validate_schema_with_files(
                schema, jya_data)
            print("paseee")

            filtered_data["professionals"] = [find_member_by_id(professional_id) for professional_id in
                                              filtered_data["professionals"]]
            print(filtered_data)
            print(files)
            create_jya(files=files + links, **filtered_data)
            return jsonify({"message": "JYA creado con éxito"}), 201
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@jyas_blueprint.route("/<int:jya_id>")
class JyaResource(MethodView):
    def get(self, jya_id):
        """
        Maneja la solicitud GET para obtener los detalles de un JYA específico.

        Returns:
            Response: Devuelve los datos del JYA en formato JSON o un mensaje de error si no se encuentra.
        """
        jya = find_jya_by_id(jya_id)
        if not jya:
            return jsonify({"message": "JYA no encontrado"}), 404

        return jsonify(jya.to_dict())

    def put(self, jya_id):
        """
        Maneja la solicitud PUT para actualizar los datos de un JYA específico.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        jya_data = extract_jyas_data()
        schema = JyAAddSchema()
        jya = find_jya_by_id(jya_id)
        if not jya:
            return jsonify({"message": "JYA no encontrado"}), 404

        try:
            filtered_data, links, files = validate_schema_with_files(
                schema, jya_data, object=jya, is_edit=True)

            filtered_data["professionals"] = [find_member_by_id(professional_id) for professional_id in
                                              filtered_data["professionals"]]

            print(filtered_data, links, files)

            for key, value in filtered_data["person"].items():
                setattr(jya.person, key, value)

            filtered_data.pop("person")
            for key, value in filtered_data.items():
                setattr(jya, key, value)

            jya.files = list(jya.files) + files + links

            print(jya.to_dict())
            db.session.commit()

            return jsonify({"message": "JYA actualizado con éxito"}), 200
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, jya_id=None):
        """
        Maneja la solicitud DELETE para eliminar un JYA específico.

        Returns:
            Response: Devuelve un mensaje de éxito si el JYA fue eliminado o un mensaje de error si no existe.
        """
        jya = find_jya_by_id(jya_id)
        if not jya:
            return jsonify({"message": "JYA no encontrado"}), 404
        for file in jya.files:
            delete_file(file)
        db.session.delete(jya)
        db.session.commit()


@jyas_blueprint.route("/<int:jya_id>/files")
class JyaFilesResource(MethodView):
    def get(self, jya_id):
        """
        Maneja la solicitud GET para obtener los archivos de un JYA específico.

        Returns:
            Response: Devuelve los datos de los archivos en formato JSON o un mensaje de error si no se encuentra.
        """
        title = request.args.get("title", None, type=str)
        type = request.args.get("type", None, type=str)
        jya = find_jya_by_id(jya_id)
        if not jya:
            return jsonify({"error": "El JYA no existe"}), 404
        return jsonify(get_filtered_files_data(jya, title=title, type=type))


def extract_jyas_data():
    """
    Extrae los datos del JYA de la solicitud.

    Returns:
        dict: Un diccionario con los datos del JYA.
    """
    files_data = extract_files_data()
    return {
        "person": {
            "name": request.form.get("name"),
            "surname": request.form.get("surname"),
            "dni": request.form.get("dni"),
            "telephone": request.form.get("telephone"),
            "emergency_contact": request.form.get("emergency_contact"),
            "address": request.form.get("address"),
        },
        "age": request.form.get("age"),
        "birth_date": request.form.get("birth_date"),
        "birth_place": request.form.get("birth_place"),
        "granted": request.form.get("granted").lower() == "true",
        "grant_percentage": request.form.get("grant_percentage", 0),
        "professionals": request.form.getlist("professionals"),
        "behind_payment": request.form.get("behind_payment").lower() == "true",
        "files": files_data,
        "links": extract_link_data()
    }
