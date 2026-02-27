from rest_framework import serializers


class ComposeSMSSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(required=False, allow_blank=True)
    recipient_phone = serializers.CharField(required=False, allow_blank=True)
    dictated_message = serializers.CharField()
    language = serializers.CharField(max_length=3, default='eng')
    session_id = serializers.CharField(required=False, default='')


class SMSActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    phone_number = serializers.CharField(allow_blank=True)
    message_body = serializers.CharField()
    recipient_name = serializers.CharField(allow_blank=True)


class ReadSMSSerializer(serializers.Serializer):
    sms_content = serializers.CharField()
    sender_name = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(max_length=3, default='eng')
