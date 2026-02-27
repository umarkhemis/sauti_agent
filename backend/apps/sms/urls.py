from django.urls import path
from .views import ComposeSMSView, ReadSMSView

urlpatterns = [
    path('compose/', ComposeSMSView.as_view(), name='sms-compose'),
    path('read/', ReadSMSView.as_view(), name='sms-read'),
]
