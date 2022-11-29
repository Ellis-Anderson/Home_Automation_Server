import json
import logging
from datetime import datetime

from flask import current_app

from .. import mqtt, scheduler, socketio
from ..models import AlarmStatus, LightStatus
from ..scheduled_events import sunrise

logger = logging.getLogger(__name__)


@socketio.on("bedroom_light_message")
def handle_light_message(data: str) -> None:
    """
    Socketio handler for 'bedroom_light_message' messages.
    Inserts updates into light_status table and propagates messages to mqtt when appropriate.

    Parameters:
    -----------
        data: str
            String that should be convertable into a json object
    """
    logger.info("received message from client: " + data)
    # Update other clients with new info
    socketio.emit("bedroom_light_message", data, broadcast=True)
    json_data = json.loads(data)
    store = json_data.pop("store")
    # If the data should be stored, add it to the db
    if store:
        LightStatus.insert_status(**json_data)
    if json_data["on_status"] == "off":
        # if the light is off just publish the 'off' light settings
        message = "0,0,0,0"
    else:
        message = ",".join(
            [str(val) for val in [json_data["red"], json_data["green"], json_data["blue"], json_data["white"]]]
        )
    mqtt.publish("bedroom/lights/cmd", message)


@socketio.on("alarm_message")
def handle_alarm_message(data: str) -> None:
    """
    Socketio handler for 'alarm_message' messages.
    Inserts updates into alarm_status table and handles alarm scheduling when appropriate.

    Parameters:
    -----------
        data: str
            String that should be convertable into a json object
    """
    logger.info("received alarm message from client: " + data)
    # Update other clients with new info
    socketio.emit("alarm_message", data, broadcast=True)
    json_data = json.loads(data)
    json_data["alarm_time"] = datetime.strptime(json_data["alarm_time"], "%H:%M").time()
    # Check if most recently scheduled job is still active, if it is remove it
    curr_job_id = AlarmStatus.query_latest_job().job_id
    res = scheduler.get_job(id=str(curr_job_id))
    if res is not None:
        logger.info(f"Removing job from scheduler {res}")
        scheduler.remove_job(id=str(curr_job_id))
    # If alarm is on schedule a new job
    if json_data["alarm_status"] == "on":
        json_data["job_id"] = curr_job_id + 1
        logger.info(
            f"Adding job {json_data['job_id']} to scheduler. "
            f"Alarm time {json_data['alarm_time'].hour}:{json_data['alarm_time'].minute}"
        )
        scheduler.add_job(
            id=str(json_data["job_id"]),
            func=sunrise,
            trigger="cron",
            hour=json_data["alarm_time"].hour,
            minute=json_data["alarm_time"].minute,
            args=[current_app._get_current_object()],  # type: ignore
        )
    AlarmStatus.insert_status(**json_data)


@socketio.on("connection")
def handle_connection(data: str) -> None:
    """On connection handler"""
    logger.info("New connection:")
    logger.info(data)
    socketio.emit("connection", "please?")


@socketio.on("disconnect")
def test_disconnect() -> None:
    """On disconnect handler"""
    logger.info("Client disconnected")
