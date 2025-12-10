from django.db import models
from django.utils import timezone
from user_agents import parse as ua_parse


class Session(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_sessions')
    token_key = models.CharField(max_length=128, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    last_active_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.token_key} for {self.user}"

    # DEVICE PARSING
    def get_parsed_device(self):
        if not self.user_agent:
            return "Unknown Device"

        ua = ua_parse(self.user_agent)

        os_name = ua.os.family
        os_version = ua.os.version_string
        browser = ua.browser.family
        device = ua.device.family or "Device"

        return f"{device} · {os_name} {os_version} · {browser}"

    # CURRENT SESSION CHECK
    def is_current(self, token_key):
        return self.token_key == token_key
