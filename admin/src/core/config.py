import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde el .env

class Config(object):
    Testing = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "abcdefg")
    SESSION_TYPE = 'filesystem'
    API_TITLE = "Cedica API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0-beta.4/swagger-ui-bundle.js"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    MINIO_SERVER = os.environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    STORAGE_BUCKET = os.environ.get("MINIO_STORAGE_BUCKET")
    DEBUG = False
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

class DevelopmentConfig(Config):
    DEBUG = True
    MINIO_SERVER = os.environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    STORAGE_BUCKET = os.environ.get("STORAGE_BUCKET")
    MINIO_SECURE = False
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
