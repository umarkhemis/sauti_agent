from rest_framework import serializers
from .models import ContactCache


class ContactSearchSerializer(serializers.Serializer):
    name_or_relationship = serializers.CharField()
    language = serializers.CharField(max_length=3, default='eng')
    session_id = serializers.CharField(required=False, default='')


class ContactResponseSerializer(serializers.Serializer):
    contacts = serializers.ListField(child=serializers.DictField())
    is_ambiguous = serializers.BooleanField()
