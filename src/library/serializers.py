from rest_framework import serializers
from .models import Book, Author, Borrow
from users.serializers import UserSerializer

# from reviews.serializers import BookReviewListSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "address", "country"]


class BookAddSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = [
            "title",
            "is_available",
            "quantity",
            "publisher",
            "genre",
            "authors",
        ]

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        book = Book.objects.create(**validated_data)
        for author_data in authors:
            author, _ = Author.objects.get_or_create(**author_data)
            book.authors.add(author)
            author.save()
        return book

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["authors"] = AuthorSerializer(
            instance.authors.all(), many=True
        ).data
        return representation

    def update(self, instance, validated_data):
        authors = validated_data.pop("authors", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if authors:
            instance.authors.clear()
            for author_data in authors:
                author, _ = Author.objects.get_or_create(**author_data)
                instance.authors.add(author)

        return instance


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "is_available",
            "quantity",
            "publisher",
            "genre",
            "created_at",
            "is_deleted",
            "authors",
            "reviews",
        ]

    def get_reviews(self, obj):
        from reviews.serializers import BookReviewListSerializer

        reviews = obj.reviews.filter(is_deleted=False).order_by("-created_at")
        return BookReviewListSerializer(
            reviews, many=True, context={"request": self.context.get("request")}
        ).data


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = [
            "users",
            "books",
            "borrow_duration",
        ]

    def create(self, validated_data):
        book = validated_data["books"]
        if not book.is_available or book.is_deleted or book.quantity <= 0:
            raise serializers.ValidationError(
                "This book is not available for borrowing."
            )
        borrow = Borrow.objects.create(**validated_data)
        book.quantity -= 1
        book.is_available = book.quantity > 0
        book.save()
        return borrow

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["users"] = {
            "id": instance.users.id,
            "email": instance.users.email,
            "first_name": instance.users.first_name,
            "last_name": instance.users.last_name,
        }
        representation["books"] = BookListSerializer(instance.books).data
        return representation

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if instance.is_returned:
            book = instance.books
            book.quantity += 1
            book.is_available = book.quantity > 0
            book.save()
        instance.save()
        return instance


class BorrowListSerializer(serializers.ModelSerializer):
    users = UserSerializer()
    books = BookListSerializer()

    class Meta:
        model = Borrow
        fields = [
            "id",
            "users",
            "books",
            "borrowed_at",
            "borrow_duration",
            "is_returned",
        ]


class BorrowUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ["is_returned"]

    def update(self, instance, validated_data):
        instance.is_returned = validated_data.get("is_returned", instance.is_returned)
        if instance.is_returned:
            book = instance.books
            book.quantity += 1
            book.is_available = book.quantity > 0
            book.save()
        instance.save()
        return instance
