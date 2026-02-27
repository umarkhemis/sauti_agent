from django.db import models


class VoiceRequest(models.Model):
    session_id = models.CharField(max_length=100)
    audio_duration_ms = models.IntegerField(default=0)
    detected_language = models.CharField(max_length=3, default='eng')
    transcribed_text = models.TextField(blank=True)
    translated_text = models.TextField(blank=True)
    processing_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VoiceRequest {self.session_id} @ {self.created_at}"
