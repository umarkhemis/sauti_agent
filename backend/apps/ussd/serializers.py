from rest_framework import serializers
from .models import USSDRequest


class USSDCodeSerializer(serializers.Serializer):
    intent = serializers.CharField()
    telecom = serializers.CharField()
    params = serializers.DictField(required=False, default=dict)


class USSDResponseSerializer(serializers.Serializer):
    raw_response = serializers.CharField()
    intent = serializers.CharField()
    language = serializers.CharField(max_length=3, default='eng')


class ParsedUSSDResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    spoken_response = serializers.CharField()
    data = serializers.DictField()
