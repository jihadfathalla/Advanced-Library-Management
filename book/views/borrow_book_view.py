from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext as _
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_exception_class import CustomException
from permissions.admin_or_librarian_permission_class import IsAdminOrLibrarian


from book.serializers.borrow_book_serializer import (
    BorrowedBookSerializer,
    ReturnBookSerializer,
)


class BorrowBookView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = BorrowedBookSerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("Book Borrowed successfully")},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)


class ReturnBookView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = ReturnBookSerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("Book Returned successfully")},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)
