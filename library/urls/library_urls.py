from django.urls import path

from library.views.library_view import (
    LibraryListView,
    LibraryCreateView,
    LibraryUpdateView,
    LibraryDeleteView,
    NearbyLibraryView,
)

urlpatterns = [
    path("create", LibraryCreateView.as_view(), name="library_create"),
    path("", LibraryListView.as_view(), name="library_list"),
    path("<int:pk>", LibraryListView.as_view(), name="library_retrieve"),
    path("<int:pk>/update", LibraryUpdateView.as_view(), name="library_update"),
    path("<int:pk>/delete", LibraryDeleteView.as_view(), name="library_delete"),
    path(
        "nearby_library/",
        NearbyLibraryView.as_view(),
        name="nearby_library",
    ),
]
