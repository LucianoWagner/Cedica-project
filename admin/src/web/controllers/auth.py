from flask import render_template, request, redirect, flash, url_for, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError

from core.auth import find_user_by_email_and_password, find_user_by_email, create_user
from flask import session

from core.bcrypt import bcrypt
from core.google_oauth import oauth
from web.handlers.auth import is_authenticated
from web.schemas.auth import LoginSchema

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/login")
class LoginResource(MethodView):
    """
        Recurso para gestionar el inicio de sesión de los usuarios.

        Métodos:
            get: Renderiza la página de inicio de sesión si el usuario no está autenticado.
            post: Maneja el envío del formulario de inicio de sesión, validando los datos
                  y autenticando al usuario.
    """

    def get(self):
        """
                Renderiza la página de inicio de sesión.

                Si el usuario ya está autenticado, lo redirige a la página principal.

                Returns:
                    Response: Redirecciona a la página principal si está autenticado,
                              o renderiza la página de login si no lo está.
        """
        if is_authenticated(session):
            return redirect(url_for("home.HomeResource"))
        return render_template("auth/login.html")

    def post(self):
        """
                Procesa el formulario de inicio de sesión.

                Valida los datos del formulario y, si son correctos, autentica al usuario
                y lo redirige a la página principal. Si la autenticación falla, redirige
                nuevamente a la página de inicio de sesión con un mensaje de error.

                Returns:
                    Response: Redirecciona a la página principal si la autenticación es exitosa,
                              o a la página de login si los datos son incorrectos.
        """
        form_data = request.form.to_dict()
        schema = LoginSchema()

        try:
            validated_data = schema.load(form_data)

            user = find_user_by_email(validated_data["email"])

            if not user.password:
                flash("Este usuario esta registrado usando google!", "error")
                return redirect(url_for("auth.LoginResource"))

            # If user is not found, redirect to login page, else redirect to home page
            if not user or not bcrypt.check_password_hash(user.password, validated_data["password"]):
                flash("Usuario o contraseña incorrectos", "error")
                return redirect(url_for("auth.LoginResource"))

            if not user.active:
                flash("El usuario ha sido bloqueado", "error")
                return redirect(url_for("auth.LoginResource"))

            if not user.is_approved:
                flash("El usuario no ha sido aprobado", "error")
                return redirect(url_for("auth.LoginResource"))

            session["user"] = user.id
            session["role"] = user.role
            session["permissions"] = user.role.permissions.all()

            print(session["permissions"])

            return redirect(url_for("home.HomeResource"))

        except ValidationError as err:
            abort(400, messages=err.messages)


@auth_blueprint.route("/logout")
class LogoutResource(MethodView):
    """
        Recurso para gestionar el cierre de sesión de los usuarios.

        Métodos:
            get: Cierra la sesión del usuario autenticado y lo redirige a la página de login.
    """

    def get(self):
        """
                Cierra la sesión del usuario autenticado.

                Elimina los datos del usuario de la sesión y redirige a la página de login.

                Returns:
                    Response: Redirecciona a la página de inicio de sesión.
        """
        if is_authenticated(session):
            del session["user"]
            session.clear()
        return redirect(url_for("auth.LoginResource"))


@auth_blueprint.route("/login/google")
class GoogleLoginResource(MethodView):
    """
        Recurso para gestionar el inicio de sesión con Google.

        Métodos:
            get: Redirige al usuario a la página de autenticación de Google.
    """

    def get(self):
        """
                Redirige al usuario a la página de autenticación de Google.

                Returns:
                    Response: Redirecciona a la página de autenticación de Google.
        """
        return oauth.google.authorize_redirect(url_for("auth.GoogleCallbackResource", _external=True))


@auth_blueprint.route("/google/callback")
class GoogleCallbackResource(MethodView):
    """
        Recurso para gestionar la respuesta de Google al inicio de sesión.

        Métodos:
            get: Procesa la respuesta de Google y autentica al usuario.
    """

    def get(self):
        """
                Procesa la respuesta de Google y autentica al usuario.

                Si la autenticación es exitosa, redirige al usuario a la página principal.
                Si la autenticación falla, redirige al usuario a la página de inicio de sesión.

                Returns:
                    Response: Redirecciona a la página principal si la autenticación es exitosa,
                              o a la página de login si los datos son incorrectos.
        """
        try:
            token = oauth.google.authorize_access_token()
            user_info = oauth.google.get("userinfo").json()
            email = user_info["email"]
            alias = user_info["name"] or user_info["email"].split("@")[0]
            if not email:
                flash("Error al iniciar sesión con Google", "error")
                return redirect(url_for("auth.LoginResource"))

            user = find_user_by_email(email)
            if not user:
                new_user = create_user(email=email, alias=alias, password=None, role_id=None, member_id=None,
                                       is_approved=False)
                flash(
                    "Usuario creado con éxito. Esperando aprovacion del administrador", "success")
                return redirect(url_for("auth.LoginResource"))

            else:
                if user.password:
                    flash(
                        "Este usuario esta registrado usando el sistema de autenticacion de la aplicacion!", "error")
                    return redirect(url_for("auth.LoginResource"))
                if not user.active:
                    flash("El usuario ha sido bloqueado", "error")
                    return redirect(url_for("auth.LoginResource"))

                if not user.is_approved:
                    flash("Tu cuenta todavia no ha sido aprobada.!", "error")
                    return redirect(url_for("auth.LoginResource"))

                session["user"] = user.id
                session["role"] = user.role
                session["permissions"] = user.role.permissions.all()
                return redirect(url_for("home.HomeResource"))

        except Exception as e:
            current_app.logger.error(e)
            flash("Error al iniciar sesión con Google", "error")
            return redirect(url_for("auth.LoginResource"))
