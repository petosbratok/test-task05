from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
import pytz

from .models import *
from .tasks import create_messages_task, send_messages_task

class CreateClientAPI(APIView):
    # Example: http://127.0.0.1:8000/create-client/?phone=799999499998&operator_code=345&tag=super&timezone=GB
    def get(self, request):
        phone = request.GET.get('phone')
        operator_code = request.GET.get('operator_code')
        tag = request.GET.get('tag')
        timezone = request.GET.get('timezone')

        if 79999999999 > int(phone) > 70000000000 and phone and operator_code and tag and timezone:
            data = {
            'phone' : phone,
            'operator_code' : operator_code,
            'tag': tag,
            'timezone': timezone,
            'info': 'New client have been created'
            }

            client = Client(
                phone=phone,
                operator_code=operator_code,
                tag=tag,
                timezone=timezone
            )
            client.save()

            return Response(data)
        return Response({'error': 'Not enought data provided'})

class UpdateClientAPI(APIView):
    # Example http://127.0.0.1:8000/update-client/?id=1&phone=76665554441
    def get(self, request):
        changed_values = {}

        try:
            client = Client.objects.get(id=request.GET.get('id'))
        except:
            return Response({'Error': 'No client was found with given id'})

        phone = request.GET.get('phone')
        operator_code = request.GET.get('operator_code')
        tag = request.GET.get('tag')
        timezone = request.GET.get('timezone')

        if 79999999999 > int(phone) > 70000000000:
            client.phone = int(phone)
            changed_values['phone'] = int(phone)
        if operator_code:
            client.operator_code = operator_code
            changed_values['operator_code'] = operator_code
        if tag:
            client.tag = tag
            changed_values['tag'] = tag
        if timezone:
            client.timezone = timezone
            changed_values['timezone'] = timezone

        client.save()

        if len(changed_values) > 0:
            return Response(changed_values)

        return Response({'Error': 'Client was found but no properties have been changed'})

class DeleteClientAPI(APIView):
    # Example http://127.0.0.1:8000/delete-client/?id=2
    def get(self, request):
        id = request.GET.get('id')

        try:
            client = Client.objects.get(id=id)
        except:
            return Response({'Error': 'No client was found with given id'})

        client.delete()
        return Response({'Info': f'Client with id {id} has been deleted'})


class CreateMailingAPI(APIView):
    def get(self, request):
        date_start = request.GET.get('date_start')
        text = request.GET.get('text')
        filter = request.GET.get('filter')
        date_end = request.GET.get('date_end')

        if not (date_start and text and filter and date_end):
            return Response({'error': 'Not enought data provided'})

        try:
            date_start_object = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        except:
            return Response({'error': 'Start date format is incorrect. Try something like this: %Y-%m-%d %H:%M:%S'})

        try:
            date_end_object = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        except:
            return Response({'error': 'Start date format is incorrect. Try something like this: %Y-%m-%d %H:%M:%S'})

        data = {
        'date_start' : date_start,
        'text' : text,
        'filter': filter,
        'date_end': date_end,
        'info': 'New mailing have been created'
        }

        mailing = Mailing(
            date_start=date_start,
            text=text,
            filter=filter,
            date_end=date_end
        )
        mailing.save()

        utc=pytz.UTC
        date_start_object = date_start_object.replace(tzinfo=utc)
        date_end_object = date_end_object.replace(tzinfo=utc)

        if datetime.now().replace(tzinfo=utc) < date_end_object:
            create_messages_task.apply_async(
                (mailing.id, 'Scheduled'),
                time_limit=5,
                soft_time_limit=2
            )

            send_messages_task.apply_async(
                (mailing.id,),
                eta=date_start_object,
                time_limit=5,
                soft_time_limit=2
            )

            data['Status'] = 'Sending' if date_start_object < datetime.now().replace(tzinfo=utc) else 'Scheduled'
        else:
            create_messages_task.apply_async(
                (mailing.id, 'Expired'),
                time_limit=5,
                soft_time_limit=2
            )
            data['Status'] = 'Expired'

        return Response(data)

class UpdateMailingAPI(APIView):
    # Example http://127.0.0.1:8000/update-client/?id=1&phone=76665554441
    def get(self, request):
        changed_values = {}

        try:
            mailing = Mailing.objects.get(id=request.GET.get('id'))
        except:
            return Response({'Error': 'No mailing was found with given id'})

        date_start = request.GET.get('date_start')
        text = request.GET.get('text')
        filter = request.GET.get('filter')
        date_end = request.GET.get('date_end')

        try:
            if date_start:
                datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
        except:
            return Response({'error': 'Start date format is incorrect. Try something like this: %Y-%m-%d %H:%M:%S'})

        try:
            if date_end:
                datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
        except:
            return Response({'error': 'End date format is incorrect. Try something like this: %Y-%m-%d %H:%M:%S'})

        if date_start:
            mailing.date_start = date_start
            changed_values['date_start'] = date_start
        if date_end:
            mailing.date_end = date_end
            changed_values['date_end'] = date_end
        if text:
            mailing.text = text
            changed_values['text'] = text
        if filter:
            mailing.filter = filter
            changed_values['filter'] = filter

        mailing.save()

        if len(changed_values) > 0:
            return Response(changed_values)

        return Response({'Error': 'Client was found but no properties have been changed'})

class DeleteMailingAPI(APIView):
    def get(self, request):
        id = request.GET.get('id')

        try:
            mailing = Mailing.objects.get(id=id)
        except:
            return Response({'Error': 'No mailing was found with given id'})

        mailing.delete()
        return Response({'Info': f'Mailing with id {id} has been deleted'})

class MailingDataOverall(APIView):
    def get(self, request):
        mailings = Mailing.objects.all()
        messages = Message.objects.all()

        data = {
            'Total mailings': len(mailings),
            'Total messages': len(messages),
            'Expired': 0,
            'Scheduled': 0,
            'Sent': 0,
            'Failed': 0,
        }

        for mailing in mailings:
            messages_filtered = messages.filter(mailing_id=mailing.id)
            for message in messages_filtered:
                data[message.delivery_status] += 1

        return Response(data)

class MailingDataSingle(APIView):
    def get(self, request):
        id = request.GET.get('id')

        try:
            mailing = Mailing.objects.get(id=id)
        except:
            return Response({'Error': 'No mailing was found with given id'})

        messages = Message.objects.filter(mailing_id=mailing.id)

        data = {
            'Total messages': len(messages),
            'Date start': mailing.date_start,
            'Date end': mailing.date_end,
            'Text': mailing.text,
            'Filter': mailing.filter,
            'Expired': 0,
            'Scheduled': 0,
            'Sent': 0,
            'Failed': 0,
        }

        for message in messages:
            data[message.delivery_status] += 1

        return Response(data)
