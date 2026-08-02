from flask import Flask

from app.database.db import db

from flask_migrate import Migrate

from app.config import Config
from app.routes.chat import chat_bp
from flask_cors import CORS



migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    app.register_blueprint(chat_bp)

    migrate.init_app(
        app,
        db
    )

    from app import models

    return app