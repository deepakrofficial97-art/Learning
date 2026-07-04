import logging
import os
import importlib
import pkgutil
from flask import Flask, Blueprint
from config import Config
from extensions import db, jwt, mail, cors, cache, migrate
import models
import routes


def register_blueprints(app: Flask, base_url: str):
    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f"routes.{module_name}")

        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            if isinstance(attr, Blueprint):
                url_prefix = f"{base_url}/{module_name}"
                app.register_blueprint(attr, url_prefix=url_prefix)
                print(f"  ✅ Registered: {attr.name} → {url_prefix}")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Logging
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

    # Upload folder
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, origins=Config.CORS_ORIGINS)
    cache.init_app(app, config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": Config.REDIS_HOST,
        "CACHE_REDIS_PORT": Config.REDIS_PORT,
        "CACHE_DEFAULT_TIMEOUT": Config.CACHE_TIMEOUT
    })
    migrate.init_app(app, db)

    # Auto-register all blueprints
    register_blueprints(app, Config.API_BASE_URL)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])

