import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'your_task_name',  # Замените 'action' на имя вашей задачи
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # Помните, что если ваша задача не принимает аргументы, вы можете пропустить 'args'
        # 'args': (agrs),  # Уберите эту строчку, если ваша задача не принимает аргументы
    },
}
