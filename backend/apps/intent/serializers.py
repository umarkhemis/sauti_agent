from rest_framework import serializers
from .models import IntentLog


class ClassifyIntentSerializer(serializers.Serializer):
    text = serializers.CharField()
    context = serializers.DictField(required=False, default=dict)
    session_id = serializers.CharField(required=False, default='')


class IntentResponseSerializer(serializers.Serializer):
    intent = serializers.CharField()
    entities = serializers.DictField()
    confidence = serializers.FloatField()
    requires_clarification = serializers.BooleanField()
    clarification_question = serializers.CharField(allow_null=True)
