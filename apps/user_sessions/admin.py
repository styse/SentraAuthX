from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "token_key_short",
        "ip_address",
        "device",
        "created_at",
        "last_active_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("user__email", "user__phone", "token_key", "ip_address", "user_agent")
    ordering = ("-created_at",)

    def token_key_short(self, obj):
        return obj.token_key[:8]
    token_key_short.short_description = "Token"

    def device(self, obj):
        return obj.get_parsed_device()
    device.short_description = "Device"
