from dataclasses import dataclass
from flask import render_template


@dataclass
class Error:
    code: int
    message: str
    description: str
    redirect: str
    redirect_text: str


def not_found_error(e):
    """
    Maneja el error 404 (No encontrada).

    Args:
        e (Exception): La excepción que causó el error.

    Returns:
        Response: Renderiza la plantilla de error con el código 404.
    """
    error = Error(404, "No encontrada", "La URL solicitada no ha sido encontrada.", "home.HomeResource",
                  "Volver a inicio")
    return render_template("error.html", error=error), 404


def unauthorized_error(e):
    """
    Maneja el error 401 (No autorizado).

    Args:
        e (Exception): La excepción que causó el error.

    Returns:
        Response: Renderiza la plantilla de error con el código 401.
    """
    error = Error(401, "No autorizado", "No estas autorizado para visitar esta pagina.", "auth.LoginResource",
                  "Ir a inicio de sesion")
    return render_template("error.html", error=error), 401
