from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Установим переменные окружения для настройки брокера и результатов
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_lms.settings')

app = Celery('your_project')

# Настроим Celery на использование Redis
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживает задачи в приложениях Django
app.autodiscover_tasks()

# Периодические задачи для celery-beat
app.conf.beat_schedule = {
    # Пример: задача, которая будет запускаться каждый день в 12:00
    'task_name': {
        'task': 'my_lms.tasks.deactivate_inactive_users',
        'schedule': crontab(minute=0, hour=12),
    },
}
