from flask import Flask


from app.db import db, migrate
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    from .routes import main_route
    app.register_blueprint(main_route)
    # with app.app_context():
    #     start_background_loader()

    return app
