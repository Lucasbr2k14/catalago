from .front import front
from .api import api

blueprints = [
    front,
    api
]

def register_blueprint(app):
    for b in blueprints:
        app.register_blueprint(b)