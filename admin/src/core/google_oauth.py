from authlib.integrations.flask_client import OAuth

oauth = OAuth()  # Create a global OAuth instance


def init_app(app):
    """
    Initialize Google OAuth with the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    oauth.init_app(app)

    google = oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        authorize_params=None,
        access_token_params=None,
        refresh_token_url=None,
        client_kwargs={"scope": "profile email"},
        jwks_url='https://www.googleapis.com/oauth2/v3/certs',
        server_metadata_url=app.config["GOOGLE_DISCOVERY_URL"],
    )
    return google
