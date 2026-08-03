from flask import Flask, app

from app.database.db import db

from flask_migrate import Migrate

from app.config import Config
from app.routes.chat import chat_bp
from flask_cors import CORS
from app.ml.model_loader import MLModelLoader
from app.ml.routes.ml_routes import ml_bp

migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    app.register_blueprint(chat_bp)
    app.register_blueprint(ml_bp)
    with app.app_context():
        MLModelLoader.load(app)

    migrate.init_app(
        app,
        db
    )
    print("\n========== REGISTERED ROUTES ==========")

    for rule in app.url_map.iter_rules():
        print(rule)

    print("=======================================\n")

    from app import models

    return app