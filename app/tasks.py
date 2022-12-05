from app.celery import app
from .models import *
from datetime import datetime
from django.db.models import Q
import pytz
import requests

utc = pytz.UTC


@app.task
def create_messages_task(id, delivery_status):
    mailing = Mailing.objects.get(id=id)

    filter = mailing.filter

    try:
        clients = Client.objects.filter(Q(operator_code=int(filter)) | Q(tag=filter)
                                        )
    except Exception:
        clients = Client.objects.filter(Q(tag=filter))

    for client in clients:
        Message.objects.create(
            mailing_id=mailing,
            client_id=client,
            delivery_status=delivery_status,
        )


@app.task
def send_messages_task(mailing_id):
    messages = Message.objects.filter(mailing_id=mailing_id)
    text = Mailing.objects.get(id=mailing_id).text

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE0MjgzMDMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6InBzYnRvayJ9.MqIJeb1A699lvLFBHFTnu8qJXZA6ifk-JUzOwOvfTxA',
        'Content-Type': 'application/json',
    }

    for message in messages:
        send_message.delay(headers, message.id, text)


@app.task
def send_message(headers, message_id, text):
    message = Message.objects.get(id=message_id)
    json_data = {
        'id': 1,
        'phone': message.client_id.phone,
        'text': text,
    }

    try:
        response = requests.post(
            'https://probe.fbrq.cloud/v1/send/1', headers=headers, json=json_data, timeout=3)
    except Exception:
        message.delivery_status = 'Failed'
        message.save()
        return

    message.delivery_status = 'Sent' if response.status_code == 200 else 'Failed'

    message.date_created = datetime.now()
    message.save()
