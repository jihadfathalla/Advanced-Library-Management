from django.db.models import Count, Q
from django.db import models
from django.db.models import Prefetch


from utils.generate_list_cache_key import generate_list_cache_key
from config.cache_function import getKey, setKey

from user.models import User
from book.models.book_model import Book


class Author(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", blank=True
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def list(cls, request):
        library_id = request.GET.get("library")
        category_id = request.GET.get("category")

        book_filter = Q()
        if library_id:
            book_filter &= Q(books__inventory__branch__library_id=library_id)
        if category_id:
            book_filter &= Q(books__category_id=category_id)

        cache_key = generate_list_cache_key(cls.__name__, book_filter)
        cached_data = getKey(cache_key)
        if cached_data is not None:
            return cached_data

        authors = cls.objects.all()
        authors = authors.annotate(
            book_count=Count("books", filter=book_filter, distinct=True)
        )
        setKey(cache_key, authors, timeout=60 * 120)
        return authors

    @classmethod
    def list_with_books(cls, request):

        filter_dict = {}
        if request.GET.get("library_id"):
            filter_dict["books__inventory__branch__library_id"] = request.GET.get(
                "library_id"
            )
        if request.GET.get("category_id"):
            filter_dict["books__category_id"] = request.GET.get("category_id")

        cache_key = generate_list_cache_key(cls.__name__, filter_dict)
        cached_data = getKey(cache_key)
        if cached_data is not None:
            return cached_data

        authors = (
            cls.objects.filter(**filter_dict)
            .prefetch_related(
                Prefetch(
                    "books",
                    queryset=Book.objects.select_related("category"),
                )
            )
            .distinct()
        )
        setKey(cache_key, authors, timeout=60 * 120)
        return authors
