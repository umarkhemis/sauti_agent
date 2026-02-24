from rest_framework import serializers


class ProcessVoiceSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language = serializers.CharField(max_length=3, default='eng')
    session_id = serializers.CharField(required=False, default='')


class DialogueResponseSerializer(serializers.Serializer):
    response_text = serializers.CharField()
    audio_response = serializers.CharField(allow_null=True)
    action_taken = serializers.CharField(allow_null=True)
    requires_input = serializers.BooleanField()
    session_id = serializers.CharField()


class ParseUSSDSerializer(serializers.Serializer):
    raw_response = serializers.CharField()
    intent = serializers.CharField()
    language = serializers.CharField(max_length=3, default='eng')
