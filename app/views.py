from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import *
from .tasks import create_messages_task

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
            return Response({'error': 'Start date has incorrect format. Format is like this: %Y-%m-%d %H:%M:%S'})

        try:
            date_end_object = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        except:
            return Response({'error': 'Start date has incorrect format. Format is like this: %Y-%m-%d %H:%M:%S'})

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

        create_messages_task.apply_async(
            (mailing.id,),
            eta=date_start_object,
            time_limit=5,
            soft_time_limit=2
        )

        return Response(data)
