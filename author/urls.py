from django.urls import path

from .views import (
    AuthorListView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
)

urlpatterns = [
    path("create", AuthorCreateView.as_view(), name="author_create"),
    path("", AuthorListView.as_view(), name="author_list"),
    path("<int:pk>", AuthorListView.as_view(), name="author_retrieve"),
    path("<str:details>", AuthorListView.as_view(), name="author_retrieve"),
    path("<int:pk>/update", AuthorUpdateView.as_view(), name="author_update"),
    path("<int:pk>/delete", AuthorDeleteView.as_view(), name="author_delete"),
]
