import locale
from datetime import datetime
from enum import member

from flask import render_template, session, abort, request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from core.database import db
from core.files import extract_link_data, extract_files_data, create_file, upload_files, process_edit_files, \
    get_filtered_files_data
from core.people import get_members, get_members_quantity, get_all_job_positions, create_member, Person, Member, \
    create_person, find_member_by_id, delete_member
from web.controllers.users import generate_pagination
from web.handlers.auth import is_authenticated, login_required, permission_required
from web.schemas.members import MemberAddSchema

members_blueprint = Blueprint("members", __name__, url_prefix="/members")


@members_blueprint.route("/")
class MembersResource(MethodView):
    @login_required
    @permission_required('team_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de miembros.

        Returns:
            Response: Renderiza la plantilla con la lista de miembros y la paginación.
        """
        page = request.args.get("page", 1, type=int)
        per_page = 10
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")
        criteria = request.args.get("criteria")
        search = request.args.get("search", None)
        job_position = request.args.get("job_position", None)
        file_types = ["Titulo", "Copia DNI", "CV actualizado",
                      "Certificado de antecedentes", "Certificado de salud"]

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        members = get_members(page=page, per_page=per_page, sort_by=sort_by, order=order, criteria=criteria,
                              search=search, job_position=job_position)

        columns = [
            {"name": "nombre", "label": "Nombre", "sortable": True},
            {"name": "apellido", "label": "Apellido", "sortable": True},
            {"name": "dni", "label": "DNI", "sortable": False},
            {"name": "email", "label": "Email", "sortable": False},
            {"name": "job_position", "label": "Puesto de Trabajo", "sortable": False},
            {"name": "created_at", "label": "Fecha de Creacion", "sortable": True}]

        count = get_members_quantity()
        total_pages = (count + per_page - 1) // per_page
        pagination = generate_pagination(page, total_pages)
        job_positions = get_all_job_positions()

        return render_template("members/members.html", data=members.items, pagination=pagination, columns=columns,
                               count=count, total_pages=total_pages,
                               page=page, per_page=per_page,
                               sort_by=sort_by, order=order,
                               criteria=criteria, search=search, job_position=job_position, job_positions=job_positions,
                               file_types=file_types)

    @permission_required("team_create")
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo miembro.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        member_data = extract_members_data()

        form_data = request.form.to_dict()

        schema = MemberAddSchema()
        schema.context = {"start_date": form_data.get(
            "start_date")}  # Set the context here
        try:
            validated_data = schema.load(
                {key: value for key, value in member_data.items()})
            client = current_app.storage.client  # No 'context' argument here

            files = []
            links = [create_file(link["link_url"], link['link_name'],
                                 link['link_type'], True)
                     for link in validated_data["links"]]
            upload_files(client, validated_data['files'], files)

            filtered_data = {key: value for key, value in validated_data.items() if
                             key not in ['files', 'links']}
            create_member(files=files + links, **filtered_data)

            return jsonify({"message": "Miembro creado con éxito"}), 201
        except ValidationError as err:
            return jsonify({"message": "La fecha de inicio no puede ser posterior a la fecha de finalización"}), 400

    @members_blueprint.route('/<int:member_id>', methods=['DELETE'])
    @login_required
    @permission_required("team_destroy")
    def delete_member(member_id):
        """
        Maneja la solicitud DELETE para eliminar un miembro por su ID.

        Args:
            member_id (int): ID del miembro a eliminar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        member = Member.query.get(member_id)
        if not member:
            return jsonify({"error": "El miembro no existe"}), 404
        if member.user:
            return jsonify({"error": "El miembro tiene un usuario asociado"}), 400

        if delete_member(member):
            return jsonify({"message": "Pago eliminado con exito"}), 204
        return jsonify({"error": "El miembro no existe"}), 404

    @members_blueprint.route("/<int:member_id>", methods=["GET"])
    @login_required
    @permission_required('team_show')
    def get_member_by_id(member_id):
        """
        Maneja la solicitud GET para obtener los detalles de un miembro específico.

        Args:
            member_id (int): ID del miembro a obtener.

        Returns:
            Response: Devuelve los detalles del miembro en formato JSON.
        """
        member = Member.query.filter_by(id=member_id).first()

        if not member:
            abort(404, description="Member not found")

        return jsonify(member.to_dict())

    @members_blueprint.route('/<int:member_id>', methods=['PUT'])
    @login_required
    @permission_required('team_update')
    def update_member(member_id):
        """
        Maneja la solicitud PUT para actualizar los datos de un miembro específico.

        Args:
            member_id (int): ID del miembro a actualizar.

        Returns:
            Response: Devuelve un mensaje de éxito o error en formato JSON.
        """
        try:
            member_data = extract_members_data()
            form_data = request.form.to_dict()

            schema = MemberAddSchema()
            schema.context = {"start_date": form_data.get(
                "start_date")}  # Set the context
            validated_data = schema.load(
                {key: value for key, value in member_data.items()})
            client = current_app.storage.client

            member = find_member_by_id(member_id)
            if not member:
                return jsonify({"error": "El miembro no existe"}), 404
            for file in member.files:
                process_edit_files(file, validated_data, client)

            new_files = []
            new_links = [create_file(link['link_url'], link['link_name'],
                                     link['link_type'], True)
                         for link in validated_data["links"]]
            upload_files(client, validated_data['files'], new_files)
            filtered_data = {key: value for key, value in validated_data.items() if
                             key not in ["files", "links"]}
            for key, value in filtered_data.items():
                setattr(member, key, value)

            member.files = list(member.files) + new_files + new_links
            db.session.commit()

            return jsonify({"message": "Miembro actualizado con exito"}), 200
        except ValidationError as err:
            return jsonify({"message": "La fecha de inicio no puede ser posterior a la fecha de finalización"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400


@members_blueprint.route("/members/<int:member_id>/files")
class MemberFilesResource(MethodView):
    def get(self, member_id):
        """
        Maneja la solicitud GET para obtener los archivos de un miembro específico.

        Args:
            member_id (int): ID del miembro.

        Returns:
            Response: Devuelve los archivos del miembro en formato JSON.
        """
        title = request.args.get("title", None, type=str)
        type = request.args.get("type", None, type=str)
        member = find_member_by_id(member_id)
        if not member:
            return jsonify({"error": "El miembro no existe"}), 404
        return jsonify(get_filtered_files_data(member, title=title, type=type))


def extract_members_data():
    """
    Extrae los datos del miembro de la solicitud.

    Returns:
        dict: Un diccionario con los datos del miembro.
    """
    files_data = extract_files_data()
    return {
        "person": {
            "name": request.form.get("name"),
            "surname": request.form.get("surname"),
            "dni": request.form.get("dni"),
            "address": request.form.get("address"),
            "telephone": request.form.get("telephone"),
            "emergency_contact": request.form.get("emergency_contact")
        },
        "email": request.form.get("email"),
        "locality": request.form.get("locality"),
        "profession": request.form.get("profession"),
        "job_position": request.form.get("job_position"),
        "start_date": request.form.get("start_date"),
        "end_date": request.form.get("end_date"),
        "medical_insurance": request.form.get("medical_insurance"),
        "insurance_number": request.form.get("insurance_number"),
        "job_condition": request.form.get("job_condition"),
        "active": request.form.get("active").lower() == "true",
        "files": files_data,
        "links": extract_link_data()
    }
