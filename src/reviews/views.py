from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BookReview
from .serializers import (
    BookReviewAddSerializer,
    BookReviewSerializer,
)
from lms.utils.response import api_response


class BookReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BookReviewAddSerializer,
    )
    def post(
        self: "BookReviewAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = BookReviewAddSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return api_response(
                data=serializer.data,
                message="Book review added successfully",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            message="Book review addition failed",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BookReviewSerializer(many=True),
        }
    )
    def get(
        self: "BookReviewAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        user = request.user

        if user.is_superuser:
            book_reviews = BookReview.objects.filter(is_deleted=False).order_by(
                "-created_at"
            )
        else:
            book_reviews = BookReview.objects.filter(
                user=user, is_deleted=False
            ).order_by("-created_at")
        serializer = BookReviewSerializer(book_reviews, many=True)
        return api_response(
            data=serializer.data,
            message="Book reviews retrieved successfully",
            status_code=status.HTTP_200_OK,
        )


class SpecificBookReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BookReviewSerializer,
        }
    )
    def get(
        self: "SpecificBookReviewAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            book_review = BookReview.objects.get(id=id, is_deleted=False)
            if not request.user.is_superuser and book_review.user != request.user:
                return Response(
                    {"detail": "You do not have permission to view this review."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = BookReviewSerializer(book_review)
            return api_response(
                data=serializer.data,
                message="Book review retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except BookReview.DoesNotExist:
            return api_response(
                message="Book review not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
