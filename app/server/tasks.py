import os
import time

from celery import Celery

from app.server import db
from app.server.models.measurement import Measurement

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="process_measurement")
def process_measurement(forecast_at, category_id, unit_id, value, sensor_id):
    measurement = Measurement(
        forecast_at=forecast_at,
        category_id=category_id,
        unit_id=unit_id,
        value=value,
        sensor_id=sensor_id,
    )
    db.session.add(measurement)
    db.session.commit()