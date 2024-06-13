import os
import logging.config

from celery import Celery

from app.settings import LOGGING


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

logging.config.dictConfig(LOGGING)
app = Celery('app')

app.conf.update(worker_redirect_stdouts=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_transport_options = {'visibility_timeout': 43200}
app.conf.result_backend_transport_options = {'visibility_timeout': 43200}
app.conf.visibility_timeout = 43200

app.conf.result_backend_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}

app.autodiscover_tasks()
