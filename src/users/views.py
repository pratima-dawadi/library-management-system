from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserLoginSerializer
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
