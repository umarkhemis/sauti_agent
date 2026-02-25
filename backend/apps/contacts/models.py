from django.db import models


class ContactCache(models.Model):
    user_session = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    telecom = models.CharField(max_length=10, blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact_name} ({self.phone_number})"
