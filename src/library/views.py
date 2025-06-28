from typing import Any


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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
from lms.permissions import IsLibrarianOrReadOnly, IsAdminOrLibrarian
from lms.utils.response import api_response
from lms.utils.pagination import CustomPagination


class BookAPIView(APIView):

    permission_classes = [IsLibrarianOrReadOnly]

    @swagger_auto_schema(
        request_body=BookAddSerializer,
    )
    def post(
        self: "BookAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:

        serializer = BookAddSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return api_response(
                data=serializer.data,
                message="Book added successfully",
                status_code=status.HTTP_201_CREATED,
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
        books = Book.objects.filter(is_deleted=False).order_by("-created_at")
        serializer = BookListSerializer(books, many=True)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(books, request)

        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return api_response(
            data=serializer.data,
            message="Books retrieved successfully",
            status_code=status.HTTP_200_OK,
        )


class SpecificBookAPIView(APIView):

    permission_classes = [IsLibrarianOrReadOnly]

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
            return api_response(
                data=serializer.data,
                message="Book retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Book.DoesNotExist:
            return api_response(
                message="Book not found", status_code=status.HTTP_404_NOT_FOUND
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
                return api_response(
                    data=serializer.data,
                    message="Book updated successfully",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return api_response(
                    message="Book update failed",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        except Book.DoesNotExist:
            print("not found ")
            return api_response(
                message="Book not found", status_code=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema()
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
            return api_response(
                message="Book deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        except Book.DoesNotExist:
            return api_response(
                message="Book not found", status_code=status.HTTP_404_NOT_FOUND
            )


class SpecificBookBorrowAPIView(APIView):
    permission_classes = [IsAdminOrLibrarian]

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

            paginator = CustomPagination()
            page = paginator.paginate_queryset(borrows, request)

            if page is not None:
                return paginator.get_paginated_response(serializer.data)

            return api_response(
                data=serializer.data,
                message="Borrowed books retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Book.DoesNotExist:
            return api_response(
                message="Book not found", status_code=status.HTTP_404_NOT_FOUND
            )


class BorrowAPIView(APIView):

    permission_classes = [IsLibrarianOrReadOnly]

    @swagger_auto_schema(request_body=BorrowSerializer)
    def post(
        self: "BorrowAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = BorrowSerializer(data=request.data, context={"request": request})
        try:
            if serializer.is_valid():
                serializer.save()
                return api_response(
                    data=serializer.data,
                    message="Borrowed book successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            return api_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except serializer.ValidationError as e:
            return api_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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
        try:
            user = request.user
            if user.is_superuser or user.role == "librarian":
                borrowed_books = Borrow.objects.all().order_by("-borrowed_at")
            else:
                borrowed_books = Borrow.objects.filter(users=user).order_by(
                    "-borrowed_at"
                )
            serializer = BorrowListSerializer(borrowed_books, many=True)

            paginator = CustomPagination()
            page = paginator.paginate_queryset(borrowed_books, request)

            if page is not None:
                return paginator.get_paginated_response(serializer.data)

            return api_response(
                data=serializer.data,
                message="Borrowed books retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Borrow.DoesNotExist:
            return api_response(
                message="No borrowed books found",
                status_code=status.HTTP_404_NOT_FOUND,
            )


class BorrowUpdateAPIView(APIView):
    permission_classes = [IsAdminOrLibrarian]

    @swagger_auto_schema(
        request_body=BorrowUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Borrow updated successfully",
                schema=BorrowUpdateSerializer,
            )
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
            user = request.user
            if user.is_superuser or user.role == "librarian":
                borrow = Borrow.objects.get(id=id)
            else:
                borrow = Borrow.objects.get(id=id, users=user)

            serializer = BorrowUpdateSerializer(borrow, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return api_response(
                    data=serializer.data,
                    message="Borrow updated successfully",
                    status_code=status.HTTP_200_OK,
                )
        except Borrow.DoesNotExist:
            return api_response(
                message="Borrow not found", status_code=status.HTTP_404_NOT_FOUND
            )
