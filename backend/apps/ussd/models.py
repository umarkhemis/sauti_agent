from django.db import models


class USSDRequest(models.Model):
    session_id = models.CharField(max_length=100)
    ussd_code = models.CharField(max_length=200, blank=True)
    telecom = models.CharField(max_length=10)
    intent = models.CharField(max_length=100)
    raw_response = models.TextField(blank=True)
    parsed_response = models.JSONField(default=dict)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"USSD {self.intent} ({self.session_id})"
