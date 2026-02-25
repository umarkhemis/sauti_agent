from django.db import models


class SMSLog(models.Model):
    DIRECTION_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    session_id = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=200, blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)
    message_body = models.TextField(blank=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='sent')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS to {self.recipient_name or self.recipient_phone} ({self.status})"
