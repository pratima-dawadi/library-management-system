from rest_framework import serializers
from .models import BookReview
from users.serializers import UserSerializer
from library.serializers import BookListSerializer


class BookReviewAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = [
            "book",
            "rating",
            "comment",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        book_review = BookReview.objects.create(user=user, **validated_data)
        return book_review


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookListSerializer()

    class Meta:
        model = BookReview
        fields = [
            "id",
            "book",
            "user",
            "rating",
            "comment",
            "created_at",
            "is_deleted",
        ]
