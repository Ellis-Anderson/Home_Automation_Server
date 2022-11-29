import logging
from typing import Any

from paho.mqtt.client import Client

from .. import mqtt

logger = logging.getLogger(__name__)


@mqtt.on_connect()
def handle_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    mqtt.subscribe("bedroom/lights/#")
    mqtt.publish("devices/checkin", "web_server checkin")


@mqtt.on_log()
def handle_logging(client: Client, userdata: Any, level: int, buf: str) -> None:
    logger.info(buf)
