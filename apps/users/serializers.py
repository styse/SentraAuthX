from rest_framework import serializers
from .models import User, OTP

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
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        email = attrs.get('email')

        if not phone and not email:
            raise serializers.ValidationError("Phone or email is required.")

        user = None
        if phone:
            user = User.objects.filter(phone=phone).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        attrs['user'] = user
        return attrs


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get('phone')
        email = attrs.get('email')
        code = attrs.get('code')

        if not phone and not email:
            raise serializers.ValidationError("Phone or email is required.")

        user = None
        if phone:
            user = User.objects.filter(phone=phone).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        otp = OTP.objects.filter(user=user, code=code, is_used=False).first()
        if not otp or otp.is_expired():
            raise serializers.ValidationError("Invalid or expired OTP.")

        attrs['user'] = user
        attrs['otp'] = otp
        return attrs