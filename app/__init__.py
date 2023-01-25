from flask import Flask
from app.config import DevelopmentConfig
from .station import station
from .journey import journey

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(DevelopmentConfig())

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(station)
    app.register_blueprint(journey)
    return app