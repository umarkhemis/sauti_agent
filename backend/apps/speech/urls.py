from django.urls import path
from .views import TranscribeView, DetectLanguageView, TextToSpeechView, TranslateView

urlpatterns = [
    path('transcribe/', TranscribeView.as_view(), name='speech-transcribe'),
    path('detect-language/', DetectLanguageView.as_view(), name='speech-detect-language'),
    path('tts/', TextToSpeechView.as_view(), name='speech-tts'),
    path('translate/', TranslateView.as_view(), name='speech-translate'),
]
