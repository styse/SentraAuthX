from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView
from django.utils import timezone
from .models import OTP, User
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer,
    OTPRequestSerializer, OTPVerifySerializer
    )
import random


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token = AuthToken.objects.create(user)[1]

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
            },
            "token": token
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = AuthToken.objects.create(user)[1]

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
            },
            "token": token
        }, status=status.HTTP_200_OK)


class LogoutView(KnoxLogoutView):
    permission_classes = ()
    pass

class LogoutAllView(KnoxLogoutAllView):
    permission_classes = ()
    pass


class RequestOTPView(generics.GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        user = User.objects.get(phone_number=phone)

        # Generate OTP
        code = str(random.randint(100000, 999999))
        OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )

        # TODO: Send OTP via SMS provider
        print(f"OTP for {phone}: {code}")

        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_instance = serializer.validated_data['otp_instance']
        otp_instance.is_used = True
        otp_instance.save()

        token = AuthToken.objects.create(otp_instance.user)[1]

        return Response({
            "user": {
                "id": otp_instance.user.id,
                "phone_number": otp_instance.user.phone_number,
                "email": otp_instance.user.email,
            },
            "token": token
        }, status=status.HTTP_200_OK)
