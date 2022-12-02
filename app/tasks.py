from app.celery import app

from .services import create_messages


@app.task
def create_messages_task(id):
    create_messages(id)
