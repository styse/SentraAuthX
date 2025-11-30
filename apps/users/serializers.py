from rest_framework import serializers
from .models import User, OTP
from django.utils import timezone

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('phone', 'email', 'password')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user()
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not phone and not email:
            raise serializers.ValidationError("Email or phone is required.")

        if email:
            user = User.objects.filter(email=email).first()
        else:
            user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        
        attrs['user'] = user
        return attrs


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def validate_phone(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number does not exist.")
        return value


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        try:
            otp = OTP.objects.get(phone=phone, code=code, is_used=False)
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        if otp.expires_at < timezone.now():
            raise serializers.ValidationError("OTP expired.")

        attrs['otp_instance'] = otp
        return attrs
