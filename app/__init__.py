from flask import Flask
from .routes import index_blueprint
from .database import DataBase
from .errors import register_errors
from configs import Configs

from .services import SegurityService


def create_app(configs:Configs) -> Flask:
    app = Flask(__name__)

    app.extensions["configs"] = configs

    app.extensions["db"] = DataBase(
        host=app.extensions["configs"].postgres_host,
        port=app.extensions["configs"].postgres_port,
        user=app.extensions["configs"].postgres_user,
        password=app.extensions["configs"].postgres_pass,
        dbname=app.extensions["configs"].postgres_datb
    )

    app.register_blueprint(index_blueprint)
    register_errors(app)

    return app