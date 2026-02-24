from django.db import models


class CallLog(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    session_id = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    telecom = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Call to {self.contact_name or self.phone_number} ({self.status})"
