import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')
# celery will look for tasks.py file in each application directory to load asynchronous tasks defined in it
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
