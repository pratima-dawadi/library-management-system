from django.db import models
from users.models import User


class Author(models.Model):
    class Meta:
        db_table = "authors"

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)


class Book(models.Model):
    class Meta:
        db_table = "books"

    title = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    publisher = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    authors = models.ManyToManyField(Author, related_name="books", blank=True)


class Borrow(models.Model):
    class Meta:
        db_table = "borrows"

    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")
    books = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    borrow_duration = models.IntegerField(default=15)
    is_returned = models.BooleanField(default=False)

