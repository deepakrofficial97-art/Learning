import json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "config.json")) as f:
    config_data = json.load(f)

db = config_data["DATABASE"]
jwt = config_data["JWT"]
log = config_data["LOGGING"]
email = config_data["EMAIL"]
upload = config_data["UPLOAD"]
redis = config_data["REDIS"]
cors = config_data["CORS"]
api = config_data["API"]
third_party = config_data["THIRD_PARTY"]


class Config:
    # App
    APP_NAME = config_data.get("APP_NAME")
    ENV = config_data.get("ENV", "development")
    DEBUG = config_data.get("DEBUG", False)
    TESTING = config_data.get("TESTING", False)
    SECRET_KEY = config_data.get("SECRET_KEY")
    HOST = config_data.get("HOST", "0.0.0.0")
    PORT = config_data.get("PORT", 5000)

    # Database
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{db['USERNAME']}:{db['PASSWORD']}"
        f"@{db['HOST']}:{db['PORT']}/{db['DATABASE_NAME']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = jwt.get("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = jwt.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30) * 60
    JWT_REFRESH_TOKEN_EXPIRES = jwt.get("REFRESH_TOKEN_EXPIRE_DAYS", 7) * 86400

    # Logging
    LOG_LEVEL = log.get("LEVEL", "INFO")
    LOG_FILE = log.get("FILE", "logs/app.log")

    # Email
    MAIL_SERVER = email.get("SMTP_SERVER")
    MAIL_PORT = email.get("SMTP_PORT", 587)
    MAIL_USERNAME = email.get("USERNAME")
    MAIL_PASSWORD = email.get("PASSWORD")
    MAIL_USE_TLS = True

    # Upload
    UPLOAD_FOLDER = upload.get("UPLOAD_FOLDER", "uploads/")
    MAX_CONTENT_LENGTH = upload.get("MAX_CONTENT_LENGTH", 16777216)
    ALLOWED_EXTENSIONS = set(upload.get("ALLOWED_EXTENSIONS", []))

    # Redis
    REDIS_HOST = redis.get("HOST", "localhost")
    REDIS_PORT = redis.get("PORT", 6379)
    CACHE_TIMEOUT = config_data.get("CACHE_TIMEOUT", 300)

    # CORS
    CORS_ORIGINS = cors.get("ORIGINS", ["*"])

    # API
    API_VERSION = api.get("VERSION", "v1")
    API_BASE_URL = api.get("BASE_URL", "/api/v1")

    # AWS / Third Party
    AWS_ACCESS_KEY = third_party.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = third_party.get("AWS_SECRET_KEY")
    S3_BUCKET = third_party.get("S3_BUCKET")
    STRIPE_API_KEY = third_party.get("STRIPE_API_KEY")

    