from rest_framework import serializers
from .models import CallLog


class ResolveCallSerializer(serializers.Serializer):
    contact_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    session_id = serializers.CharField(required=False, default='')


class CallActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    phone_number = serializers.CharField()
    contact_name = serializers.CharField(allow_blank=True)


class LogCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['session_id', 'contact_name', 'phone_number', 'telecom', 'status']
