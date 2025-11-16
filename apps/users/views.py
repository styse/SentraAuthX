from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView
from .serializers import UserRegisterSerializer, UserLoginSerializer


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
