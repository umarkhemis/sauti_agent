from rest_framework import serializers
from .models import VoiceRequest


class TranscribeSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language = serializers.CharField(max_length=3, default='eng')


class DetectLanguageSerializer(serializers.Serializer):
    audio = serializers.FileField()


class TranscribeResponseSerializer(serializers.Serializer):
    text = serializers.CharField()
    confidence = serializers.FloatField()
    language = serializers.CharField()


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField(max_length=3, default='eng')


class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField()
    source_language = serializers.CharField(max_length=3)
    target_language = serializers.CharField(max_length=3)
