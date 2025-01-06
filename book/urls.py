from django.urls import path

from .views.book_view import (
    BookListView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)
from .views.borrow_book_view import (
    BorrowBookView,
    ReturnBookView,
)

urlpatterns = [
    path("create", BookCreateView.as_view(), name="book_create"),
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>", BookListView.as_view(), name="book_retrieve"),
    path("<int:pk>/update", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete", BookDeleteView.as_view(), name="book_delete"),
    path("borrow", BorrowBookView.as_view(), name="book_borrow"),
    path("return", ReturnBookView.as_view(), name="book_return"),
]
