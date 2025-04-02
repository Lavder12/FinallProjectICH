from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from web_room.models import Announcement  # Импортируем правильную модель

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey("web_room.Announcement", on_delete=models.CASCADE)

    viewed_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-viewed_at']

