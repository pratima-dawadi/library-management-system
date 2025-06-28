from django.core.management.base import BaseCommand
from users.models import User
from library.models import Author, Book


class Command(BaseCommand):
    help = "Seed the database with admin, librarian, authors, and books"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding admin and librarian users...")

        admin, _ = User.objects.get_or_create(
            email="admin@gmail.com",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
                "role": "admin",
            },
        )
        admin.set_password("admin123")
        admin.save()

        librarian, _ = User.objects.get_or_create(
            email="librarian@gmail.com",
            defaults={
                "first_name": "Ram",
                "last_name": "Librarian",
                "is_staff": True,
                "is_superuser": False,
                "role": "librarian",
            },
        )
        librarian.set_password("lib123")
        librarian.save()

        self.stdout.write("Seeding authors...")

        authors_data = [
            {
                "first_name": "Parijat",
                "last_name": "",
                "address": "Kathmandu",
                "country": "Nepal",
            },
            {
                "first_name": "Laxmi Prasad",
                "last_name": "Devkota",
                "address": "Kathmandu",
                "country": "Nepal",
            },
            {
                "first_name": "Narayan",
                "last_name": "Wagle",
                "address": "Kaski",
                "country": "Nepal",
            },
            {
                "first_name": "Subin",
                "last_name": "Bhattarai",
                "address": "Kathmandu",
                "country": "Nepal",
            },
        ]

        authors = []
        for data in authors_data:
            author, _ = Author.objects.get_or_create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults={
                    "address": data["address"],
                    "country": data["country"],
                },
            )
            authors.append(author)

        self.stdout.write("Seeding books...")

        books_data = [
            {
                "title": "Muna Madan",
                "quantity": 8,
                "publisher": "Sajha Prakashan",
                "genre": "Epic Poetry",
                "author_indices": [1],
            },
            {
                "title": "Shirishko Phool",
                "quantity": 6,
                "publisher": "Nepali Sahitya Parishad",
                "genre": "Fiction",
                "author_indices": [0],
            },
            {
                "title": "Palpasa Cafe",
                "quantity": 5,
                "publisher": "Nepalaya Publication",
                "genre": "Fiction",
                "author_indices": [2],
            },
            {
                "title": "Summer Love",
                "quantity": 4,
                "publisher": "FinePrint",
                "genre": "Romance",
                "author_indices": [3],
            },
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                defaults={
                    "quantity": book_data["quantity"],
                    "is_available": book_data["quantity"] > 0,
                    "publisher": book_data["publisher"],
                    "genre": book_data["genre"],
                },
            )
            if created:
                selected_authors = [authors[i] for i in book_data["author_indices"]]
                book.authors.set(selected_authors)

        self.stdout.write(self.style.SUCCESS("Data seeded successfully!"))
