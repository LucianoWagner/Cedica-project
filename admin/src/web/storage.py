from minio import Minio


class Storage:
    """Clase para manejar la conexión con el servidor Minio."""

    def __init__(self, app=None):
        """
        Inicializa la instancia de Storage.

        Args:
            app (Flask, optional): La aplicación Flask. Por defecto es None.
        """
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Inicializa la aplicación Flask con la configuración de Minio.

        Args:
            app (Flask): La aplicación Flask.

        Returns:
            Flask: La aplicación Flask configurada.
        """
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", True)
        self._client = Minio(minio_server, access_key=access_key, secret_key=secret_key,
                             secure=secure)  # inicializa el cliente de minio
        app.storage = self  # se agrega el objeto storage al objeto app y asi se puede acceder a el desde cualquier parte de la aplicacion
        return app

    @property
    def client(self):
        """
        Obtiene el cliente de Minio.

        Returns:
            Minio: El cliente de Minio.
        """
        return self._client

    @client.setter
    def client(self, value):
        """
        Establece el cliente de Minio.

        Args:
            value (Minio): El cliente de Minio.
        """
        self._client = value


storage = Storage()
