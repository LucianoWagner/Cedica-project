from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import inspect, text

from core.database import db
from core.seeds import run_seed, seed_data

db_blueprient = Blueprint("db", __name__, url_prefix="/db")


@db_blueprient.route("/seed")
class SeedResource(MethodView):
    def get(self):
        """
        Ejecuta el proceso de sembrado de datos en la base de datos.
        """
        try:
            seed_data()
            return jsonify({"message": "Se han sembrado los datos exitosamente."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@db_blueprient.route("/truncate")
class ClearResource(MethodView):
    def get(self):
        """
        Elimina todos los datos de la base de datos en PostgreSQL.
        """
        try:
            # Use SQLAlchemy inspector to get table names
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()

            table_names = [
                table for table in table_names if table != "alembic_version"]

            # Disable constraints by dropping and recreating tables
            for table in table_names:
                db.session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))

            db.session.commit()
            return jsonify({"message": "Se han eliminado todos los datos exitosamente."}), 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return jsonify({"error": str(e)}), 500
