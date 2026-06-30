from flask import Flask, Blueprint, render_template, g
from .routes import index_blueprint
from .database import DataBase


import json

def create_app() -> Flask:
    app = Flask(__name__)

    app.db = DataBase()

    app.register_blueprint(index_blueprint)

    return app