from rest_framework import serializers
from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    device = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "id",
            "token_key",
            "ip_address",
            "device",
            "user_agent",
            "created_at",
            "last_active_at",
            "is_active",
            "is_current",
        ]

    def get_device(self, obj):
        return obj.get_parsed_device()

    def get_is_current(self, obj):
        request = self.context.get("request")
        if not request or not request.auth:
            return False
        return obj.token_key == str(request.auth)[:32]