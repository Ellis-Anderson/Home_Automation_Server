import logging
from typing import Any

from sqlalchemy import func, select

from . import db

logger = logging.getLogger(__name__)


class LightStatus(db.Model):  # type: ignore
    """
    light_status table

    Attributes:
    -----------
        id: int
            autoincrementing primary key
        time_updated: DateTime = sqlalchemy.func.now()
            date and time entry was added
        red: int
            red color value
        green: int
            green color value
        blue: int
            blue color value
        white: int
            white color value
        on_status: bool
            True if light is on else False

    Methods:
    --------
        insert_status(**kwargs): -> None
            Add an entry based on passed keyword args
        query_current_status(): -> Any
            Query the most recent entry in the table
    """

    __tablename__ = "light_status"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    time_updated = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    red = db.Column(
        db.Integer,
        nullable=False,
    )
    green = db.Column(db.Integer, nullable=False)
    blue = db.Column(db.Integer, nullable=False)
    white = db.Column(db.Integer, nullable=False)
    on_status = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return (
            "\nlight_status:\n"
            f"\tred: {self.red}\n"
            f"\tgreen: {self.green}\n"
            f"\tblue: {self.blue}\n"
            f"\twhite: {self.white}\n"
            f"\tstatus: {self.on_status}"
        )

    @classmethod
    def insert_status(cls, **kwargs: Any) -> None:
        """Insert an instance of LightStatus into table"""
        logger.info(f"posting data {kwargs} to table {cls.__table__.name}")
        update = cls(**kwargs)
        db.session.add(update)
        db.session.commit()

    @classmethod
    def query_current_status(cls) -> Any:
        """Query most recent light_status update"""
        subquery = select(func.max(cls.id)).scalar_subquery()
        row = db.session.query(cls).filter(cls.id == subquery).first()
        logger.debug(row)
        return row


class AlarmStatus(db.Model):  # type: ignore
    """
    alarm_status table:

    Attributes:
    -----------
        id: Optional[int]
            autoincrementing primary key
        time_updated: Optional[DateTime] = sqlalchemy.func.now()
            date and time entry was added
        alarm_time: Time
            time alarm is set for
        alarm_status: bool
            True if alarm is on else False
        job_id: Optional[int]
            Identifier for most recent scheduled job for working with scheduler

    Methods:
    --------
        insert_status(**kwargs): -> None
            Add an entry based on passed keyword args
        query_current_status(): -> Any
            Query the most recent entry in the table
        query_latest_job(): -> Any
            Query the most recently scheduled job
    """

    __table_name__ = "alarm_status"
    id = db.Column(db.Integer, primary_key=True)
    time_updated = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    alarm_time = db.Column(db.Time, nullable=False)
    alarm_status = db.Column(db.Text, nullable=False)
    job_id = db.Column(db.Integer)

    def __repr__(self) -> str:
        return (
            "\nalarm_status:\n"
            f"\ttime_updated: {self.time_updated}\n"
            f"\talarm_time: {self.alarm_time}\n"
            f"\talarm_status: {self.alarm_status}\n"
            f"\tjob_id: {self.job_id}"
        )

    @classmethod
    def insert_status(cls, **kwargs: Any) -> None:
        """Insert an instance of AlarmStatus into table"""
        logger.info(f"posting data {kwargs} to table {cls.__table__.name}")
        update = cls(**kwargs)
        db.session.add(update)
        db.session.commit()

    @classmethod
    def query_current_status(cls) -> Any:
        """Query the most recent alarm_status update"""
        subquery = select(func.max(cls.id)).scalar_subquery()
        logger.debug(subquery)
        row = db.session.query(cls).filter(cls.id == subquery).first()
        logger.debug(row)
        return row

    @classmethod
    def query_latest_job(cls) -> Any:
        """Query the most recent alarm_status update that was scheduled"""
        subquery = select(func.max(cls.job_id)).scalar_subquery()
        logger.debug(subquery)
        row = db.session.query(cls).filter(cls.job_id == subquery).first()
        logger.debug(row)
        return row
