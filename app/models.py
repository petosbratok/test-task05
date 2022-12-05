from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import pytz


class Mailing(models.Model):
    date_start = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    filter = models.CharField(blank=True, max_length=100)
    date_end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:50]


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone = models.IntegerField(validators=[
        MaxValueValidator(79999999999),
        MinValueValidator(70000000000)
    ])
    operator_code = models.IntegerField()
    tag = models.CharField(max_length=100)
    timezone = models.CharField(
        max_length=32, choices=TIMEZONES, default='Europe/Moscow')

    def __str__(self):
        return f'Code: {self.operator_code}; Tag: {self.tag}'


class Message(models.Model):
    date_created = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(blank=True, max_length=100)
    mailing_id = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, null=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.delivery_status} / Scheduled at: {str(self.mailing_id.date_start)[5:16]} / Sent at: {str(self.date_created)[5:16] if self.date_created else "not sent"};'
