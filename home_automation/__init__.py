import logging

import eventlet
from blinker import Namespace
from flask import Flask
from flask_apscheduler import APScheduler
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

eventlet.monkey_patch()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

socketio = SocketIO()
mqtt = Mqtt()
db = SQLAlchemy()
scheduler = APScheduler()
event_signals = Namespace()
sunrise_signal = event_signals.signal("sunrise")


def init_app() -> Flask:
    """Create and initialize the Flask app appropriately"""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        from .home import home_bp

        app.register_blueprint(home_bp)
        db.create_all()
        mqtt.init_app(app)
        socketio.init_app(app)
        scheduler.init_app(app)
        scheduler.start()

    return app
