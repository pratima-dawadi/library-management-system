from django.urls import path
from .views import (
    BookAPIView,
    SpecificBookAPIView,
    BorrowAPIView,
    BorrowUpdateAPIView,
    SpecificBookBorrowAPIView,
)


urlpatterns = [
    path("books/", BookAPIView.as_view(), name="book-api"),
    path("books/<int:id>/", SpecificBookAPIView.as_view(), name="book-detail-api"),
    path(
        "books/<int:id>/borrow/",
        SpecificBookBorrowAPIView.as_view(),
        name="specific-book-borrow-api",
    ),
    path("borrow/", BorrowAPIView.as_view(), name="borrow-api"),
    path("borrow/<int:id>/", BorrowUpdateAPIView.as_view(), name="borrow-update-api"),
]
