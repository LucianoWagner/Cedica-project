from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app):
    """
    Initialize bcrypt
    param app: Flask app
    """
    bcrypt.init_app(app)
