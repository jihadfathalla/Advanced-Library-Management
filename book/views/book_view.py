from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext as _
from utils.get_model_by_pk import get_model_by_pk
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_paginator import paginate_queryset
from utils.custom_exception_class import CustomException
from permissions.admin_or_librarian_permission_class import IsAdminOrLibrarian


from book.models.book_model import Book
from book.serializers.book_serializer import BookListSerializer, BookCreateSerializer


class BookListView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = BookListSerializer

    @handle_exceptions
    def get(self, request, pk=None):
        try:
            if pk:
                book = get_model_by_pk("book", "Book", pk)
                serializer = self.serializer_class(book)
                return Response(serializer.data)
            else:
                books = Book.list(request)
                return paginate_queryset(request, books, self.serializer_class)
        except:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=self.serializer_class.errors,
            )


class BookCreateView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = BookCreateSerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("Book is successfully created")},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)


class BookUpdateView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = BookCreateSerializer

    @handle_exceptions
    def patch(self, request, pk):
        book = get_model_by_pk("book", "Book", pk)

        serializer = self.serializer_class(
            instance=book, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Book updated successfully")}, status=200)
        raise CustomException(status_code=400, errors=serializer.errors)


class BookDeleteView(APIView):
    permission_classes = [IsAdminOrLibrarian]

    @handle_exceptions
    def delete(self, request, pk):
        book = get_model_by_pk("book", "Book", pk)
        book.delete()
        return Response(data={"message": _("Book deleted successfully")})
