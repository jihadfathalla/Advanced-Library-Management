from django.db import models

from utils.generate_list_cache_key import generate_list_cache_key
from config.cache_function import getKey, setKey

from library.models.library_branch_model import Category


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        "author.Author", related_name="books", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, related_name="books", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    @classmethod
    def list(cls, request):
        library_id = request.GET.get("library_id")
        category_id = request.GET.get("category_id")
        author_id = request.GET.get("author_id")
        available = request.GET.get("available")

        filter_dict = {}
        if library_id:
            filter_dict["inventory__branch__library_id"] = library_id
        if category_id:
            filter_dict["category"] = category_id
        if author_id:
            filter_dict["author"] = author_id
        if available:
            filter_dict["available"] = available

        cache_key = generate_list_cache_key(cls.__name__, filter_dict)
        cached_data = getKey(cache_key)
        if cached_data is not None:
            return cached_data
        books = cls.objects.filter(**filter_dict)
        setKey(cache_key, books, timeout=60 * 15)
        return books
