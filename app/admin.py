from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)
