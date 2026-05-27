from celery import Celery
from celery.schedules import crontab

from settings import settings


celery_app = Celery(
    "advantageous_view",
    broker=settings.redis.url,
    backend=settings.redis.url,
    include=["infrastructure.celery_app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    beat_schedule={
        "check-prices-daily": {
            "task": "check_prices",
            "schedule": crontab(hour=0, minute=0),
        },
    },
    worker_pool="prefork",
)
