import json
import logging
from datetime import datetime

from flask import current_app

from .. import mqtt, scheduler, socketio
from ..models import AlarmStatus, LightStatus
from ..scheduled_events import sunrise

logger = logging.getLogger(__name__)


@socketio.on("bedroom_light_message")
def handle_light_message(data):
    logger.info("received message from client: " + data)
    socketio.emit("bedroom_light_message", data, broadcast=True)
    data = json.loads(data)
    store = data.pop("store")
    if store:
        LightStatus.insert_status(**data)
    if data["on_status"] == "off":
        message = "0,0,0,0"
    else:
        message = ",".join([str(val) for val in [data["red"], data["green"], data["blue"], data["white"]]])
    mqtt.publish("bedroom/lights/cmd", message)


@socketio.on("alarm_message")
def handle_alarm_message(data):
    logger.info("received alarm message from client: " + data)
    socketio.emit("alarm_message", data, broadcast=True)
    data = json.loads(data)
    data["alarm_time"] = datetime.strptime(data["alarm_time"], "%H:%M").time()
    curr_job_id = AlarmStatus.query_latest_job().job_id
    res = scheduler.get_job(id=str(curr_job_id))
    if res is not None:
        logger.info(f"Removing job from scheduler {res}")
        scheduler.remove_job(id=str(curr_job_id))
    if data["alarm_status"] == "on":
        data["job_id"] = curr_job_id + 1
        logger.info(
            f"Adding job {data['job_id']} to scheduler. "
            f"Alarm time {data['alarm_time'].hour}:{data['alarm_time'].minute}"
        )
        scheduler.add_job(
            id=str(data["job_id"]),
            func=sunrise,
            trigger="cron",
            hour=data["alarm_time"].hour,
            minute=data["alarm_time"].minute,
            args=[current_app._get_current_object()],
        )
    AlarmStatus.insert_status(**data)


@socketio.on("connection")
def handle_connection(data):
    logger.info("New connection:")
    logger.info(data)
    socketio.emit("connection", "please?")


@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")
