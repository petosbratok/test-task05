from .models import *
from datetime import datetime
from django.db.models import Q
import pytz

utc=pytz.UTC

def create_messages(id, delivery_status):
    mailing = Mailing.objects.get(id=id)

    date_end = mailing.date_end.replace(tzinfo=utc)
    date_start = mailing.date_start.replace(tzinfo=utc)

    filter = mailing.filter

    try:
        clients = Client.objects.filter(
            Q(operator_code=int(filter)) |
            Q(tag=filter)
        )
    except:
        clients = Client.objects.filter(Q(tag=filter))

    for client in clients:
        Message.objects.create(
            mailing_id=mailing,
            client_id=client,
            delivery_status=delivery_status,
        )

def send_messages(id):
    messages = Message.objects.filter(mailing_id=id)

    for message in messages:
        message.delivery_status = 'Sent'
        message.date_created=datetime.now()
        message.save()
