from app.celery import app

from .services import create_messages, send_messages


@app.task
def create_messages_task(id, delivery_status):
    create_messages(id, delivery_status)

@app.task
def send_messages_task(id):
    send_messages(id)
