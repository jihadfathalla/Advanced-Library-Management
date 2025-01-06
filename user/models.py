from django.db import models
from haversine import haversine

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email"))
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    def get_nearby_libraries(self, library):
        user_location = (self.latitude, self.longitude)
        library_location = (library.latitude, library.longitude)
        return haversine(user_location, library_location)
