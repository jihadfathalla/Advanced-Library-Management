from django.db import models
from library.models.library_model import Library



class LibraryBranch(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="branches")
    branch_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return f"{self.branch_name} ({self.library.name})"



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
