from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserListSerializer
from lms.permissions import IsAdmin
from lms.utils.response import api_response


class UserRegisterView(APIView):

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(
        self: "UserRegisterView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                data=serializer.errors,
                message="Invalid data",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return api_response(
            data=serializer.data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(
        self: "UserLoginView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return api_response(
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            message="User logged in successfully",
            status_code=status.HTTP_200_OK,
        )


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema()
    def get(
        self: "UserListView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        try:
            users = (
                User.objects.all().exclude(is_superuser=True).order_by("-date_joined")
            )
            user_data = UserListSerializer(users, many=True).data
            return api_response(
                data=user_data,
                message="User list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return api_response(
                message=f"Error retrieving user list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TokenRefreshView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh token"
                ),
            },
        )
    )
    def post(
        self: "TokenRefreshView", request: Any, *args: Any, **kwargs: Any
    ) -> Response:
        refresh_token = request.data.get("refresh_token")

        try:
            refresh = RefreshToken(refresh_token)
            user = User.objects.get(id=refresh["user_id"])
            refresh_token = RefreshToken.for_user(user)
            return api_response(
                data={
                    "refresh_token": str(refresh_token),
                    "access_token": str(refresh_token.access_token),
                },
                message="Token refreshed successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception:
            return api_response(
                message="Invalid refresh token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
