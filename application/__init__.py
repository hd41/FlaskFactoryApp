from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_crontab import Crontab


db = SQLAlchemy()
crontab = Crontab()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    crontab.init_app(app)

    with app.app_context():
        from . import routes
        from . import another_routes

        # Create tables for our models
        db.create_all()

        return app
