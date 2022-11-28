import logging

from .. import mqtt

logger = logging.getLogger(__name__)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("bedroom/lights/#")
    mqtt.publish("devices/checkin", "web_server checkin")


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    logger.info(buf)
