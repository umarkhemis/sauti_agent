from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('lug', 'Luganda'),
        ('ach', 'Acholi'),
        ('nyn', 'Runyankole'),
        ('lso', 'Lusoga'),
        ('lgg', 'Lugbara'),
        ('eng', 'English'),
    ]
    TELECOM_CHOICES = [
        ('MTN', 'MTN Uganda'),
        ('AIRTEL', 'Airtel Uganda'),
    ]

    phone_number = models.CharField(max_length=20, blank=True)
    preferred_language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='eng')
    primary_telecom = models.CharField(max_length=10, choices=TELECOM_CHOICES, default='MTN')
    onboarding_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UserSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    detected_language = models.CharField(max_length=3, default='eng')
    current_intent = models.CharField(max_length=100, blank=True)
    session_data = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"
