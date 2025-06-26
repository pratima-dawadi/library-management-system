from django.db import models
from users.models import User
from library.models import Book


class BookReview(models.Model):
    class Meta:
        db_table = "book_reviews"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=0)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
