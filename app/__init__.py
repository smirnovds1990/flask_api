import logging
import os
import threading
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.db import db, migrate
from app.services import load_fetched_data_to_db
from config import Config


formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
if not os.path.exists("logs"):
    os.mkdir("logs")

file_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=1024*1024*10, backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models  # noqa
    from .routes import main_route
    app.register_blueprint(main_route)
    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    with app.app_context():
        threading.Thread(
            target=load_fetched_data_to_db,
            args=(app,),
            daemon=True,
        ).start()

    return app
