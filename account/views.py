from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, LoginUserSerializer

@swagger_auto_schema("auth")
class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "User created successfully",
            "status": status.HTTP_201_CREATED,
            "response": serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)



@swagger_auto_schema("auth")
class LoginUser(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken.for_user(serializer.validated_data)
        data = serializer.data
        data["token"] = {"refresh": str(token), "access": str(token.access_token)}
        response = {
            "message": "User logged in successfully",
            "status": status.HTTP_200_OK,
            "response": data,
        }
        return Response(response, status=status.HTTP_200_OK)

