from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('worker',broker='amqp://user:password@broker:5672',backend='rpc://',include=['worker.tasks'])