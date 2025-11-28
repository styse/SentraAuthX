from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer,
    OTPRequestSerializer, OTPVerifySerializer
    )
from .models import OTP


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



class RequestOTPView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_code = OTP.generate_otp()
            OTP.objects.create(user=user, code=otp_code)
            
            # TODO: send otp_code via SMS or Email
            print(f"OTP for {user}: {otp_code}")  # For testing
            
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp = serializer.validated_data['otp']
            
            otp.is_used = True
            otp.save()
            
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
