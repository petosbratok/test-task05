from django.urls import path
from django.conf.urls import url
from . import views
from .views import (
    CreateClientAPI,
    UpdateClientAPI,
    DeleteClientAPI,

    CreateMailingAPI,
    UpdateMailingAPI,
    DeleteMailingAPI,

    MailingDataOverall,
    MailingDataSingle,
)

urlpatterns = [
    url(r'^$', views.schema_view),

    path('create-client/', CreateClientAPI.as_view(), name='create-client-api'),
    path('update-client/', UpdateClientAPI.as_view(), name='update-client-api'),
    path('delete-client/', DeleteClientAPI.as_view(), name='delete-client-api'),

    path('create-mailing/', CreateMailingAPI.as_view(), name='create-mailing-api'),
    path('update-mailing/', UpdateMailingAPI.as_view(), name='update-mailing-api'),
    path('delete-mailing/', DeleteMailingAPI.as_view(), name='delete-mailing-api'),

    path('mailing-data-overall/', MailingDataOverall.as_view(), name='mailing-data-overall-api'),
    path('mailing-data-single/', MailingDataSingle.as_view(), name='mailing-data-single-api'),
]
