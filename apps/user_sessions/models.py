from django.db import models
from django.utils import timezone


class Session(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_sessions')
    token_key = models.CharField(max_length=64, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    last_active_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Session {self.token_key} for {self.user}"
    