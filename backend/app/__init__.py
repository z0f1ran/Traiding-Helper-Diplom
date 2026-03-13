from flask import Flask
from config import Config

from app.controllers import TradingController
from app.extensions import db
from app.views import api_bp


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
        TradingController().seed_data()

    return app
