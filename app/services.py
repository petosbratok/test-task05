from .models import *
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.db.models import Q
import pytz

utc=pytz.UTC

def create_messages(id):
    mailing = Mailing.objects.get(id=id)

    date_end = mailing.date_end.replace(tzinfo=utc)
    date_start = mailing.date_start.replace(tzinfo=utc)

    if date_start < datetime.now().replace(tzinfo=utc) < date_end:
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
                delivery_status='Sent',
            )
