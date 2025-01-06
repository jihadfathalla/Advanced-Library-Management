"""
URL configuration for advanced_ibrary_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from notification_channels.notify_book_returned_view import test_notify_book_returned

from permissions.create_roles_permissions import roles


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/library/", include("library.urls.library_urls")),
    path("api/category/", include("library.urls.category_urls")),
    path("api/author/", include("author.urls")),
    path("api/book/", include("book.urls")),
    path("test/", test_notify_book_returned),
    path("roles/", roles),
]
