import json
import logging
from typing import Optional

from flask import Flask

from .. import mqtt, socketio, sunrise_signal
from ..models import LightStatus

logger = logging.getLogger(__name__)


@sunrise_signal.connect
def sunrise_handler(app: Flask, msg: Optional[str] = None) -> None:
    """
    Handle messages coming from scheduler sunrise process

    Parameters:
    -----------
        app: Flask
            flask app context of the current application
        msg: Optional[str]
            message detailing information to be propagated
    """
    if msg is None:
        logger.error("Required keyword argument 'msg' was not found")
        return
    with app.app_context():
        socketio.emit("bedroom_light_message", msg, broadcast=True)
        msg_json = json.loads(msg)
        store = msg_json.pop("store")
        if store:
            LightStatus.insert_status(**msg_json)
        color_vals = [msg_json["red"], msg_json["green"], msg_json["blue"], msg_json["white"]]
        mqtt_msg = ",".join([str(val) for val in color_vals])
        mqtt.publish("bedroom/lights/cmd", mqtt_msg)
