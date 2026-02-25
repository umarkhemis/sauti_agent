import base64
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from .serializers import TranscribeSerializer, DetectLanguageSerializer, TTSSerializer, TranslateSerializer
from .sunbird_client import SunbirdClient
from .models import VoiceRequest


class TranscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TranscribeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = serializer.validated_data['audio']
        language = serializer.validated_data['language']
        audio_bytes = audio_file.read()

        start = time.time()
        client = SunbirdClient()
        result = client.transcribe(audio_bytes, language)
        elapsed = int((time.time() - start) * 1000)

        VoiceRequest.objects.create(
            session_id=request.data.get('session_id', ''),
            audio_duration_ms=0,
            detected_language=language,
            transcribed_text=result.get('text', ''),
            processing_time_ms=elapsed,
        )

        if 'error' in result:
            return Response({'success': False, 'error': result['error']}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({'success': True, 'data': {
            'text': result['text'],
            'confidence': result['confidence'],
            'language': result['language'],
        }})


class DetectLanguageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DetectLanguageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = serializer.validated_data['audio']
        audio_bytes = audio_file.read()

        client = SunbirdClient()
        result = client.detect_language(audio_bytes)

        return Response({'success': True, 'data': result})


class TextToSpeechView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TTSSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        language = serializer.validated_data['language']

        client = SunbirdClient()
        audio_bytes = client.text_to_speech(text, language)

        if not audio_bytes:
            return Response({'success': False, 'error': 'TTS generation failed'}, status=status.HTTP_502_BAD_GATEWAY)

        return HttpResponse(audio_bytes, content_type='audio/mpeg')


class TranslateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TranslateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        client = SunbirdClient()
        result = client.translate(
            serializer.validated_data['text'],
            serializer.validated_data['source_language'],
            serializer.validated_data['target_language'],
        )

        return Response({'success': True, 'data': result})
