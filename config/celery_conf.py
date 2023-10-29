from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.autodiscover_tasks()

celery_app.conf.update(
    broker_url = 'amqp://guest:guest@broker:5672',
    result_backend = 'rpc://',
    task_serializer = 'json',
    result_serializer = 'pickle',
    # accept_content = ['json', 'pickle'],
    result_expires = timedelta(days=1),
    task_always_eager = False,
    worker_prefetch_multiplier = 4
)