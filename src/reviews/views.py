from typing import Any


from drf_yasg import openapi
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

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            book_reviews = BookReview.objects.filter(is_deleted=False)
        else:
            book_reviews = BookReview.objects.filter(user=user, is_deleted=False)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except BookReview.DoesNotExist:
            return Response(
                {"detail": "Book review not found"}, status=status.HTTP_404_NOT_FOUND
            )
