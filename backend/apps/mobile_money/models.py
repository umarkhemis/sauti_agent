from django.db import models


class MobileMoneyTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('send', 'Send Money'),
        ('receive', 'Receive Money'),
        ('balance', 'Balance Check'),
        ('airtime', 'Buy Airtime'),
        ('data', 'Buy Data'),
        ('loan', 'Loan'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    TELECOM_CHOICES = [
        ('MTN', 'MTN Uganda'),
        ('AIRTEL', 'Airtel Uganda'),
    ]

    session_id = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='UGX')
    recipient_phone = models.CharField(max_length=20, blank=True)
    telecom = models.CharField(max_length=10, choices=TELECOM_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    telecom_reference = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.amount} {self.currency} ({self.status})"
