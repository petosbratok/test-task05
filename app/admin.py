from django.contrib import admin

# Register your models here.
from .models import *

class IdAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Mailing, IdAdmin)
admin.site.register(Client, IdAdmin)
admin.site.register(Message, IdAdmin)
