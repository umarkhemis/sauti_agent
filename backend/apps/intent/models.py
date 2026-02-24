from django.db import models


class IntentLog(models.Model):
    session_id = models.CharField(max_length=100)
    input_text = models.TextField()
    detected_intent = models.CharField(max_length=100)
    entities = models.JSONField(default=dict)
    confidence = models.FloatField(default=0.0)
    processing_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.detected_intent} ({self.session_id})"
