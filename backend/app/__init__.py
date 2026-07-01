from flask import Flask

from app.database.db import db

from flask_migrate import Migrate

from app.config import Config


migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    from app import models

    return app