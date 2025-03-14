import os

from flask import Flask, render_template, session
from flask_migrate import migrate, Migrate, upgrade

from sqlalchemy.orm import joinedload

from core.bcrypt import bcrypt
from core.people.people import Person
from .context import inject_nav_links
from .controllers.articles import articles_blueprint
from .controllers.auth import auth_blueprint
from .controllers.charges import charges_blueprint
from .controllers.db import db_blueprient
from .controllers.home import home_blueprint
from .controllers.horses import horses_blueprint
from .controllers.jyas import jyas_blueprint
from .controllers.members import members_blueprint
from .controllers.payments import payments_blueprint
from .controllers.users import users_blueprint
from .controllers.publications import publications_blueprint
from .controllers.messages import messages_blueprint
from .controllers.reports import reports_blueprint
from .handlers.auth import has_session_permission
from .handlers.error import not_found_error, unauthorized_error
from core import database, config, google_oauth
from flask_smorest import Api
from core.auth import *
from core.people import *
from core.files import *
from core.horses import *
from core.finance import *
from flask_session import Session
from core.seeds import run_seed, seed_data
from flask import session

from .storage import storage
from flask_cors import CORS

session_init = Session()
nav_links = [{
    "name": "JYA",
    "href": "/jya"
}, {
    "name": "Usuarios",
    "href": "/usuarios"
}]


def create_app(env="development", static_folder="../../static"):
    """
        Crea y configura la aplicación Flask.

        Args:
            env (str): El entorno de configuración (por defecto es "development").
            static_folder (str): La carpeta de archivos estáticos (por defecto es "../../static").

        Returns:
            Flask: La aplicación Flask configurada para correr.
    """
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config.config[env])
    CORS(app)
    print(os.environ.get("DATABASE_URL"))
    database.init_app(app)
    session_init.init_app(app)
    bcrypt.init_app(app)
    storage.init_app(app)
    google = google_oauth.init_app(app)
    migrate = Migrate(app, database.db)

    # with app.app_context():
    #     upgrade()

    api = Api(app)
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(home_blueprint)
    api.register_blueprint(horses_blueprint)
    api.register_blueprint(charges_blueprint)
    api.register_blueprint(payments_blueprint)
    api.register_blueprint(jyas_blueprint)
    api.register_blueprint(users_blueprint)
    api.register_blueprint(members_blueprint)
    api.register_blueprint(publications_blueprint)
    api.register_blueprint(messages_blueprint)
    api.register_blueprint(reports_blueprint)
    api.register_blueprint(articles_blueprint)
    api.register_blueprint(db_blueprient)

    app.context_processor(inject_nav_links)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(401, unauthorized_error)
    app.cli.add_command(run_seed)
    app.jinja_env.globals[
        # se consulta en los templates si el usuario tiene permisos
        'has_session_permission'] = has_session_permission

    return app
