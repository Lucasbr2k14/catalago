from .front import front


blueprints = [
    front
]


def register_blueprint(app):
    for b in blueprints:
        app.register_blueprint(b)