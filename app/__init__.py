from flask import Flask
from .routes import register_blueprint
from .database import DataBase
from .errors import register_errors
from configs import Configs

from .services import SegurityService


def create_app(configs:Configs) -> Flask:
    app = Flask(__name__)
    app.json.sort_keys = False # type:ignore
    app.extensions["configs"] = configs

    app.extensions["db"] = DataBase(
        configs.postgres_conn
    )

    register_blueprint(app)
    register_errors(app)

    return app