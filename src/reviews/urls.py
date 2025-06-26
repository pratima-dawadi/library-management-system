from django.urls import path
from .views import BookReviewAPIView, SpecificBookReviewAPIView


urlpatterns = [
    path("review/", BookReviewAPIView.as_view(), name="book-api"),
    path(
        "review/book/<int:id>/",
        SpecificBookReviewAPIView.as_view(),
        name="book-detail-api",
    ),
]
