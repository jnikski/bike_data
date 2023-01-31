from flask import Flask
from .station import station
from .journey import journey

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping({"PER_PAGE": 12})

    app.register_blueprint(station)
    app.register_blueprint(journey)

    return app
