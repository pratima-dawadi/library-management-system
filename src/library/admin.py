from django.contrib import admin

from .models import Book, Author, Borrow


admin.site.register([Book, Author, Borrow])
