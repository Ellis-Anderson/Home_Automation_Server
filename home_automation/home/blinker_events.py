import json
from typing import Any

from flask import Flask

from .. import mqtt, socketio, sunrise_signal
from ..models import LightStatus


@sunrise_signal.connect
def sunrise_handler(app: Flask, **kwargs: Any) -> None:
    message = kwargs["msg"]
    with app.app_context():
        socketio.emit("bedroom_light_message", message, broadcast=True)
        msg_json = json.loads(message)
        store = msg_json.pop("store")
        if store:
            LightStatus.insert_status(**msg_json)
        color_vals = [msg_json["red"], msg_json["green"], msg_json["blue"], msg_json["white"]]
        mqtt_msg = ",".join([str(val) for val in color_vals])
        mqtt.publish("bedroom/lights/cmd", mqtt_msg)
