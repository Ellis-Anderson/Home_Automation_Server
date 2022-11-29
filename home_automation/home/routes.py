import logging

from flask import render_template

from ..models import AlarmStatus, LightStatus
from . import home_bp

logger = logging.getLogger(__name__)


@home_bp.route("/")
def home() -> str:
    row = LightStatus.query_current_status()
    light_data = {
        "rgb": "#{0:02x}{1:02x}{2:02x}".format(row.red, row.green, row.blue),
        "brightness": row.white,
        "on_status": row.on_status.capitalize(),
    }
    alarm_data = AlarmStatus.query_current_status()
    alarm_data.alarm_time = alarm_data.alarm_time.strftime("%H:%M")
    alarm_data.alarm_status = alarm_data.alarm_status.capitalize()
    return render_template("index.html", light_data=light_data, alarm_data=alarm_data)
