from django.db import models


class ConversationTurn(models.Model):
    session_id = models.CharField(max_length=100)
    turn_number = models.IntegerField(default=1)
    user_input_text = models.TextField(blank=True)
    system_response_text = models.TextField(blank=True)
    intent = models.CharField(max_length=100, blank=True)
    action_taken = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['session_id', 'turn_number']

    def __str__(self):
        return f"Turn {self.turn_number} ({self.session_id})"
