from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
        Inicializa la aplicación con la configuración de SQLAlchemy.

        Args:
            app (Flask): La instancia de la aplicación Flask.

        Returns:
            Flask: La instancia de la aplicación Flask configurada.
    """
    db.init_app(app)
    config(app)
    return app


def config(app):
    """
        Configura la aplicación para cerrar la sesión de la base de datos al finalizar el contexto de la aplicación.

        Args:
            app (Flask): La instancia de la aplicación Flask.

        Returns:
            Flask: La instancia de la aplicación Flask configurada.
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app
