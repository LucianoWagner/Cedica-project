import locale

from flask_smorest import Blueprint
from flask import request, render_template, session, jsonify, abort
from flask.views import MethodView

from core.database import db
from core.public import get_publications, get_publications_quantity
from web.handlers.auth import login_required, permission_required
from web.handlers.pagination import generate_pagination
from core.public import Publication
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

publications_blueprint = Blueprint(
    "publications", __name__, url_prefix="/publications")


@publications_blueprint.route("/")
class PublicationsResource(MethodView):
    @login_required
    @permission_required('publication_index')
    def get(self):
        """
        Maneja la solicitud GET para obtener una lista de publicaciones.

        Returns:
            Response: Renderiza la plantilla con la lista de publicaciones y la paginación.
        """
        page = request.args.get("page", 1, type=int)
        per_page = 10
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        publications = get_publications(
            page=page, per_page=per_page, sort_by=sort_by, order=order)

        columns = [
            {"name": "publication_date", "label": "Publicación", "sortable": True},
            {"name": "created_at", "label": "Creación", "sortable": True},
            {"name": "title", "label": "Título", "sortable": True},
            {"name": "user", "label": "Autor", "sortable": False},
            {"name": "status", "label": "Estado", "sortable": False},
        ]

        count = get_publications_quantity()
        total_pages = (count + per_page - 1) // per_page
        pagination = generate_pagination(page, total_pages)

        return render_template("publications/publications.html", data=publications.items, pagination=pagination,
                               columns=columns,
                               count=count, total_pages=total_pages,
                               page=page, per_page=per_page,
                               sort_by=sort_by, order=order)

    @permission_required('publication_create')
    def post(self):
        try:
            # Get user_id from session
            user_id = session.get('user')
            if not user_id:
                return jsonify({"error": "Usuario no autenticado"}), 401

            # Extract form data
            title = request.form.get('title')
            summary = request.form.get('summary')
            content = request.form.get('content')
            status = request.form.get('status')

            VALID_STATUSES = ['Borrador', 'Archivada', 'Publicada']
            # Validate the status value
            if status not in VALID_STATUSES:
                return jsonify({"error": "Estado inválido"}), 400

            # Set publication date based on status
            if status == 'Publicada':
                publication_date = datetime.utcnow()
            else:
                publication_date = None

            print(status)

            # Create new Publication object
            new_publication = Publication(
                title=title,
                summary=summary,
                content=content,
                status=status,
                user_id=user_id,
                publication_date=publication_date,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Add and commit to database
            db.session.add(new_publication)
            db.session.commit()

            return jsonify({"message": "Publicacion agregada con exito"}), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Se produjo un error al agregar la publicacion"}), 500

        except Exception as e:
            return jsonify({"message": "Se produjo un error al agregar la publicacion"}), 500

    @publications_blueprint.route("/<int:publication_id>", methods=["GET"])
    @login_required
    @permission_required('publication_show')
    def get_publication_by_id(publication_id):
        """
        Maneja la solicitud GET para obtener los detalles de una publicación específica.

        Args:
            publication_id (int): ID de la publicación a obtener.

        Returns:
            Response: Devuelve los detalles de la publicación en formato JSON.
        """
        publication = Publication.query.filter_by(id=publication_id).first()

        if not publication:
            abort(404, description="No se encontro la publicacion")

        return jsonify(publication.to_dict())

    @publications_blueprint.route("/<int:publication_id>", methods=["PUT"])
    @login_required
    @permission_required('publication_update')
    def edit_publication(publication_id):
        try:
            # Extract form data
            title = request.form.get('title')
            summary = request.form.get('summary')
            content = request.form.get('content')
            status = request.form.get('status')

            VALID_STATUSES = ['Borrador', 'Archivada', 'Publicada']
            # Validate the status value
            if status not in VALID_STATUSES:
                return jsonify({"error": "Estado inválido"}), 400

            # Get publication object
            publication = Publication.query.filter_by(
                id=publication_id).first()

            if not publication:
                return jsonify({"error": "Publicacion no encontrada"}), 404

            # Set publication date based on status
            if status == 'Publicada' and not publication.publication_date:
                publication_date = datetime.utcnow()
            else:
                publication_date = None

            # Update publication object
            publication.title = title
            publication.summary = summary
            publication.content = content
            publication.publication_date = publication_date
            publication.status = status
            publication.updated_at = datetime.utcnow()

            # Commit to database
            db.session.commit()

            return jsonify({"message": "Publicacion actualizada con exito"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Se produjo un error al actualizar la publicacion", "details": str(e)}), 500

        except Exception as e:
            return jsonify({"message": "Se produjo un error al actualizar la publicacion", "details": str(e)}), 500

    @publications_blueprint.route("/<int:publication_id>", methods=["DELETE"])
    @login_required
    @permission_required('publication_destroy')
    def delete_publication(publication_id):
        try:
            # Get publication object
            publication = Publication.query.filter_by(
                id=publication_id).first()

            if not publication:
                return jsonify({"error": "Publicacion no encontrada"}), 404

            # Delete publication object
            db.session.delete(publication)
            db.session.commit()

            return jsonify({"message": "Publicacion eliminada con exito"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Se produjo un error al eliminar la publicacion"}), 500

        except Exception as e:
            return jsonify({"message": "Se produjo un error al eliminar la publicacion"}), 500
