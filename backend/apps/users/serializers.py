from rest_framework import serializers
from .models import User, UserSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'preferred_language',
                  'primary_telecom', 'onboarding_complete']
        read_only_fields = ['id']


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['session_id', 'detected_language', 'current_intent',
                  'session_data', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['session_id', 'created_at', 'updated_at']


class LanguagePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['preferred_language', 'primary_telecom']
