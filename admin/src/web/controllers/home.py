from flask import render_template, session, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from web.handlers.auth import is_authenticated, login_required

home_blueprint = Blueprint("home", __name__, url_prefix="/")


@home_blueprint.route("/")
class HomeResource(MethodView):
    """
        Recurso para la página principal de la aplicación.

        Esta clase maneja las solicitudes GET a la ruta principal '/'
        y renderiza la plantilla 'home.html' para los usuarios autenticados.
    """

    @login_required
    def get(self):
        """
                Maneja la solicitud GET para la ruta principal.

                Devuelve la página de inicio ('home.html') si el usuario ha iniciado sesión.
        """
        return render_template("home.html")
