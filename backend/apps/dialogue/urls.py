from django.urls import path
from .views import ProcessVoiceCommandView, ParseUSSDResponseView, GetFillerAudioView

urlpatterns = [
    path('process/', ProcessVoiceCommandView.as_view(), name='dialogue-process'),
    path('parse-ussd/', ParseUSSDResponseView.as_view(), name='dialogue-parse-ussd'),
    path('filler/<str:language>/', GetFillerAudioView.as_view(), name='dialogue-filler'),
]
