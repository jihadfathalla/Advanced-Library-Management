from django.db import models
from utils.generate_list_cache_key import generate_list_cache_key
from config.cache_function import getKey, setKey


class Library(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def list(cls, request):
        filter_dict = {}
        if request.GET.get("category"):
            filter_dict["branches__inventory__book__category_id"] = request.GET.get(
                "category"
            )
        if request.GET.get("author"):
            filter_dict["branches__inventory__book__author_id"] = request.GET.get(
                "author"
            )
        cache_key = generate_list_cache_key(cls.__name__, filter_dict)
        cached_data = getKey(cache_key)
        if cached_data is not None:
            return cached_data
        libraries = cls.objects.filter(**filter_dict).distinct()
        setKey(cache_key, libraries, timeout=60 * 15)
        return libraries
