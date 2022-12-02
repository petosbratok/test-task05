from django.urls import path
from . import views
from .views import (
    CreateClientAPI,
    UpdateClientAPI,
    DeleteClientAPI,
    CreateMailingAPI
)

urlpatterns = [
    path('create-client/', CreateClientAPI.as_view(), name='create-client-api'),
    path('update-client/', UpdateClientAPI.as_view(), name='update-client-api'),
    path('delete-client/', DeleteClientAPI.as_view(), name='delete-client-api'),
    path('create-mailing/', CreateMailingAPI.as_view(), name='create-mailing-api'),
]
