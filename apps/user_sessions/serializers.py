from rest_framework import serializers
from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id',
            'user',
            'token_key',
            'ip_address',
            'user_agent',
            'created_at',
            'last_active_at',
            'is_active'
        ]
