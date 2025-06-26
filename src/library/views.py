from typing import Any


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Borrow
from .serializers import (
    BookAddSerializer,
    BookListSerializer,
    BorrowSerializer,
    BorrowListSerializer,
    BorrowUpdateSerializer,
)
from lms.permissions import IsAdmin


class BookAPIView(APIView):

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        request_body=BookAddSerializer,
    )
    def post(
        self: "BookAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:

        serializer = BookAddSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BookListSerializer(many=True),
        }
    )
    def get(
        self: "BookAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        books = Book.objects.filter(is_deleted=False)
        serializer = BookListSerializer(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SpecificBookAPIView(APIView):

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BookListSerializer,
        }
    )
    def get(
        self: "SpecificBookAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            book = Book.objects.get(id=id, is_deleted=False)
            serializer = BookListSerializer(book)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        request_body=BookAddSerializer,
    )
    def patch(
        self: "SpecificBookAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            book = Book.objects.get(id=id, is_deleted=False)
            serializer = BookAddSerializer(book, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Book deleted successfully",
            status.HTTP_404_NOT_FOUND: "Book not found",
        }
    )
    def delete(
        self: "SpecificBookAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            book = Book.objects.get(id=id, is_deleted=False)
            book.is_deleted = True
            book.save()
            return Response(
                {"detail": "Book deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )


class SpecificBookBorrowAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema()
    def get(
        self: "SpecificBookBorrowAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            book = Book.objects.get(id=id, is_deleted=False)
            borrows = Borrow.objects.filter(books=book)

            serializer = BorrowListSerializer(borrows, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BorrowAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @swagger_auto_schema(request_body=BorrowSerializer)
    def post(
        self: "BorrowAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = BorrowSerializer(data=request.data, context={"request": request})
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"detail": "Book borrowed successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except serializer.ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Borrowed books retrieved successfully",
                schema=BorrowSerializer(many=True),
            )
        }
    )
    def get(
        self: "BorrowAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        user = request.user
        if user.is_superuser:
            borrowed_books = Borrow.objects.all().order_by("-borrowed_at")
        else:
            borrowed_books = Borrow.objects.filter(users=user).order_by("-borrowed_at")
        serializer = BorrowSerializer(borrowed_books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BorrowUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=BorrowUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Borrow updated successfully",
                schema=BorrowUpdateSerializer,
            ),
            status.HTTP_404_NOT_FOUND: "Borrow not found",
        },
    )
    def patch(
        self: "BorrowUpdateAPIView",
        request: Request,
        id: int,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        try:
            borrow = Borrow.objects.get(id=id, users=request.user)
            serializer = BorrowUpdateSerializer(borrow, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Borrow.DoesNotExist:
            return Response(
                {"detail": "Borrow not found"}, status=status.HTTP_404_NOT_FOUND
            )
