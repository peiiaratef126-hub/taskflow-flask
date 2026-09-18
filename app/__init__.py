import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

db = SQLAlchemy()


def create_app(config_name=None):
    """Application factory that initializes Flask, Database, and Blueprints."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)

    if isinstance(config_name, str):
        config_class = config_by_name.get(config_name, config_by_name["default"])
        app.config.from_object(config_class)
    else:
        app.config.from_object(config_name)

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
