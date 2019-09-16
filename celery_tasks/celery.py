from __future__ import absolute_import, unicode_literals
from celery import Celery
from Config import Config
from time import sleep

app = Celery(
    "celery",
    backend=Config().get_redis_url(),
    broker=Config().get_redis_url(),
    include=["celery_tasks.tasks"])

