from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from core.database import db
from core.public import Publication

articles_blueprint = Blueprint("articles", __name__, url_prefix="/articles")


@articles_blueprint.route("/")
class ArticlesResource(MethodView):
    def get(self):
        """
        Obtiene una lista de artículos filtrados por autor y/o rango de fechas, con paginación.
        """
        try:
            # Parámetros de consulta
            author = request.args.get("author", type=str)
            published_from = request.args.get("published_from", type=str)
            published_to = request.args.get("published_to", type=str)
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 9, type=int)

            # Construcción de consulta
            query = db.session.query(Publication).join(
                Publication.user).filter(Publication.status == "Publicada")

            # Filtro por autor
            if author:
                query = query.filter(Publication.user.has(name=author))

            # Filtro por rango de fechas
            if published_from:
                try:
                    published_from_date = datetime.fromisoformat(
                        published_from.replace("Z", "+00:00"))
                    query = query.filter(
                        Publication.publication_date >= published_from_date)
                except ValueError:
                    return jsonify({"error": "Formato de fecha inválido en 'published_from'"}), 400

            if published_to:
                try:
                    published_to_date = datetime.fromisoformat(
                        published_to.replace("Z", "+00:00"))
                    query = query.filter(
                        Publication.publication_date <= published_to_date)
                except ValueError:
                    return jsonify({"error": "Formato de fecha inválido en 'published_to'"}), 400

            # Orden y paginación
            query = query.order_by(Publication.publication_date.desc())
            paginated_results = query.paginate(
                page=page, per_page=per_page, error_out=False)

            # Construcción de respuesta
            data = [
                {
                    "title": pub.title,
                    "summary": pub.summary,
                    "content": pub.content,
                    "published_at": pub.publication_date.isoformat(),
                    "updated_at": pub.updated_at.isoformat(),
                    "author": pub.user.member.person.name + " " + pub.user.member.person.surname,
                }
                for pub in paginated_results.items
            ]

            return jsonify({
                "data": data,
                "page": page,
                "per_page": per_page,
                "total": paginated_results.total
            }), 200

        except SQLAlchemyError as e:
            return jsonify({"error": "Se produjo un error al obtener las publicaciones"}), 500

        except Exception as e:
            return jsonify({"error": "Se produjo un error al obtener las publicaciones"}), 500
