from django.urls import path

from library.views.category_view import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    path("create", CategoryCreateView.as_view(), name="category_create"),
    path("", CategoryListView.as_view(), name="category_list"),
    path("<int:pk>", CategoryListView.as_view(), name="category_retrieve"),
    path("<int:pk>/update", CategoryUpdateView.as_view(), name="category_update"),
    path("<int:pk>/delete", CategoryDeleteView.as_view(), name="category_delete"),
]
