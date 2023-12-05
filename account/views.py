from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password

from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer,
    LogoutUserSerializer,
    UserSerializer,
    PasswordChangeSerializer,
)


@swagger_auto_schema(tags=["auth"])
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


@swagger_auto_schema(tags=["auth"])
class LoginUser(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["token"] = {"refresh": str(token), "access": str(token.access_token)}
        response = {
            "message": "User logged in successfully",
            "status": status.HTTP_200_OK,
            "response": data,
        }
        return Response(response, status=status.HTTP_200_OK)


@swagger_auto_schema(tags=["auth"])
class LogoutUser(generics.GenericAPIView):
    serializer_class = LogoutUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "User logged out successfully",
            "status": status.HTTP_205_RESET_CONTENT,
        }
        return Response(response, status=status.HTTP_205_RESET_CONTENT)


@swagger_auto_schema(tags=["user"])
class GetEditUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(object)
        response = {
            "message": "User details fetched successfully",
            "status": status.HTTP_200_OK,
            "response": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(methodS=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    @swagger_auto_schema(tags=["user"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "message": "User data updated successfully",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def perform_update(self, instance):
        """save updated instance"""
        instance.save()


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.request.user
        object = self.get_object()
        serializer = self.get_serializer(object, data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data["current_password"]
        password = user.password

        if not check_password(current_password, password):
            return Response(
                {"Error": "Current Password not correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_password = serializer.validated_data["new_password"]
        
        user.set_password(new_password)
        user.save()

        response = {
            "message": "Password changed successfully",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)
