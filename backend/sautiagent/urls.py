from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/speech/', include('apps.speech.urls')),
    path('api/v1/intent/', include('apps.intent.urls')),
    path('api/v1/dialogue/', include('apps.dialogue.urls')),
    path('api/v1/ussd/', include('apps.ussd.urls')),
    path('api/v1/mobile-money/', include('apps.mobile_money.urls')),
    path('api/v1/calls/', include('apps.calls.urls')),
    path('api/v1/sms/', include('apps.sms.urls')),
    path('api/v1/contacts/', include('apps.contacts.urls')),
]
