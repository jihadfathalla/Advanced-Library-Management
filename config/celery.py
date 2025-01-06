from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("advanced_ibrary_management_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


from celery.schedules import crontab

app.conf.broker_url = "redis://localhost:6379/0"

# Load task modules from all registered Django app configs.

app.autodiscover_tasks()

# Schedule the tasks to run at time needed
app.conf.beat_schedule = {
    "send_reminders": {
        "task": "book.tasks.send_daily_reminders_task.send_reminders",
        "schedule": crontab(minute=1, hour=0),
    },
    "update_penalties": {
        "task": "book.tasks.update_penalties_task.update_penalties",
        "schedule": crontab(minute=1, hour=0),
    },
}
