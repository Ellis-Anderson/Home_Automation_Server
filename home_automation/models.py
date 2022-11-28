import logging

from sqlalchemy import func, select

from . import db

logger = logging.getLogger(__name__)


class LightStatus(db.Model):
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

    def __repr__(self):
        return (
            "\nlight_status:\n"
            f"\tred: {self.red}\n"
            f"\tgreen: {self.green}\n"
            f"\tblue: {self.blue}\n"
            f"\twhite: {self.white}\n"
            f"\tstatus: {self.on_status}"
        )

    @classmethod
    def insert_status(cls, **kwargs):
        logger.info(f"posting data {kwargs} to table {cls.__table__.name}")
        update = cls(**kwargs)
        db.session.add(update)
        db.session.commit()

    @classmethod
    def query_current_status(cls):
        subquery = select(func.max(cls.id)).scalar_subquery()
        logger.debug(subquery)
        row = db.session.query(cls).filter(cls.id == subquery).first()
        logger.debug(row)
        return row


class AlarmStatus(db.Model):
    __table_name__ = "alarm_status"
    id = db.Column(db.Integer, primary_key=True)
    time_updated = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    alarm_time = db.Column(db.Time, nullable=False)
    alarm_status = db.Column(db.Text, nullable=False)
    job_id = db.Column(db.Integer)

    def __repr__(self):
        return (
            "\nalarm_status:\n"
            f"\ttime_updated: {self.time_updated}\n"
            f"\talarm_time: {self.alarm_time}\n"
            f"\talarm_status: {self.alarm_status}\n"
            f"\tjob_id: {self.job_id}"
        )

    @classmethod
    def insert_status(cls, **kwargs):
        logger.info(f"posting data {kwargs} to table {cls.__table__.name}")
        update = cls(**kwargs)
        db.session.add(update)
        db.session.commit()

    @classmethod
    def query_current_status(cls):
        subquery = select(func.max(cls.id)).scalar_subquery()
        logger.debug(subquery)
        row = db.session.query(cls).filter(cls.id == subquery).first()
        logger.debug(row)
        return row

    @classmethod
    def query_latest_job(cls):
        subquery = select(func.max(cls.job_id)).scalar_subquery()
        logger.debug(subquery)
        row = db.session.query(cls).filter(cls.job_id == subquery).first()
        logger.debug(row)
        return row
