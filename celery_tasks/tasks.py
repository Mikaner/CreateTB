from __future__ import absolute_import, unicode_literals
from celery_tasks.celery import app
from celery.contrib.abortable import AbortableTask
import requests
import json
from datetime import datetime
from time import sleep


@app.task
def add(x, y):
    return x + y

@app.task(bind=True, base=AbortableTask)
def send_heart_beating(self, session_id, request_data):
    if self.is_aborted():
        return
        
    url = f"https://api.dmc.nico/api/sessions/{session_id}?_format=json&_method=PUT"
    headers = {
        "Content-Type": "application/json"
    }
    for _ in range(150):
        request_data = (requests.post(url, headers=headers, data=json.dumps(request_data["data"]))).json()
        sleep(10)