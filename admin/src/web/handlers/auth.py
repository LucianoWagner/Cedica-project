from functools import wraps

from flask import session, abort


def is_authenticated(session):
    """
    Verifica si el usuario está autenticado.

    Args:
        session (Session): La sesión actual.

    Returns:
        bool: True si el usuario está autenticado, False en caso contrario.
    """
    return session.get("user") is not None


def login_required(func):
    """
    Decorador que requiere que el usuario esté autenticado para acceder a la función.

    Args:
        func (function): La función a decorar.

    Returns:
        function: La función decorada.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)

        return func(*args, **kwargs)

    return wrapper


def has_session_permission(session, permission_name):
    """
    Verifica si la sesión tiene el permiso especificado.

    Args:
        session (Session): La sesión actual.
        permission_name (str): El nombre del permiso a verificar.

    Returns:
        bool: True si la sesión tiene el permiso, False en caso contrario.
    """
    return any(permission.name == permission_name for permission in session.get("permissions", []))


def permission_required(permission):
    """
    Decorador que requiere que la sesión tenga un permiso específico para acceder a la función.

    Args:
        permission (str): El nombre del permiso requerido.

    Returns:
        function: La función decorada.
    """

    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not is_authenticated(session):
                return abort(401)
            if "permissions" not in session:
                return abort(401)
            if not has_session_permission(session, permission):
                return abort(401)
            return function(*args, **kwargs)

        return decorated_function

    return decorator
