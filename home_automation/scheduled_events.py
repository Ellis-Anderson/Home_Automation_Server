import json
import logging
from typing import TypedDict

import eventlet
from flask import Flask

from . import sunrise_signal

logger = logging.getLogger(__name__)


class ColorMessage(TypedDict):
    red: int
    green: int
    blue: int
    white: int
    on_status: str
    store: bool


def sunrise(app: Flask) -> None:
    with app.app_context():
        light_map: ColorMessage = {"red": 64, "green": 16, "blue": 0, "white": 0, "on_status": "on", "store": True}

        def gen_message() -> ColorMessage:
            for color in ["red", "green", "blue", "white"]:
                assert isinstance(color, int)
                light_map[color] = light_map[color] if light_map[color] < 256 else 255
            return light_map

        sunrise_signal.send(app, msg=json.dumps(gen_message()))
        logging.info(json.dumps(gen_message()))
        eventlet.sleep(2)
        for _ in range(64):
            light_map["red"] += 2
            light_map["green"] += 1
            logging.info(json.dumps(gen_message()))
            sunrise_signal.send(app, msg=json.dumps(gen_message()))
            eventlet.sleep(2)

        for _ in range(255):
            light_map["red"] += 1
            light_map["green"] += 1
            light_map["blue"] += 1
            light_map["white"] += 1
            logging.info(json.dumps(gen_message()))
            sunrise_signal.send(app, msg=json.dumps(gen_message()))
            eventlet.sleep(2)
