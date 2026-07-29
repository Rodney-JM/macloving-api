from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "together",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "check-expired-subscriptions": {
            "task": "app.worker.tasks.check_expired_subscriptions",
            "schedule": crontab(minute=0),  # every hour
        },
        "unlock-due-surprises": {
            "task": "app.worker.tasks.unlock_due_surprises",
            "schedule": 60.0,
        },
        "cleanup-expired-tokens": {
            "task": "app.worker.tasks.cleanup_expired_tokens",
            "schedule": crontab(hour=3, minute=0),
        },
    }
)

@celery_app.task(name="app.worker.tasks.check_expired_subscriptions")
def _check_expired_subscriptions():
    from app.worker.tasks import check_expired_subscriptions
    check_expired_subscriptions()

@celery_app.task(name="app.worker.tasks.unlock_due_surprises")
def _unlock_due_surprises():
    from app.worker.tasks import unlock_due_surprises
    unlock_due_surprises()

@celery_app.task(name="app.worker.tasks.cleanup_expired_tokens")
def _cleanup_expired_tokens():
    from app.worker.tasks import cleanup_expired_tokens
    cleanup_expired_tokens()