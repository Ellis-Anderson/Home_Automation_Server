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
    """
    A job meant to be scheduled implementing a sunrise-esque light color sequence

    Parameters:
    -----------
        app: Flask
            The app context in which this process has been scheduled
    """
    with app.app_context():
        light_map: ColorMessage = {"red": 64, "green": 16, "blue": 0, "white": 0, "on_status": "on", "store": True}

        def gen_message() -> ColorMessage:
            """Create a value ceiling for colors to prevent overflow"""
            for color in ["red", "green", "blue", "white"]:
                light_map[color] = light_map[color] if light_map[color] < 256 else 255  # type: ignore
            return light_map

        # Send message to signal in main process
        msg = json.dumps(gen_message())
        sunrise_signal.send(app, msg=msg)
        logging.info(msg)
        eventlet.sleep(2)

        for _ in range(64):
            light_map["red"] += 2
            light_map["green"] += 1
            msg = json.dumps(gen_message())
            sunrise_signal.send(app, msg=msg)
            logging.info(msg)
            eventlet.sleep(2)

        for _ in range(255):
            light_map["red"] += 1
            light_map["green"] += 1
            light_map["blue"] += 1
            light_map["white"] += 1
            msg = json.dumps(gen_message())
            sunrise_signal.send(app, msg=msg)
            logging.info(msg)
            eventlet.sleep(2)
