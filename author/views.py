from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext as _
from utils.get_model_by_pk import get_model_by_pk
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_paginator import paginate_queryset
from utils.custom_exception_class import CustomException
from utils.custom_throttle_class import CustomRateThrottle
from permissions.admin_permission_class import IsAdmin


from author.serializer import AuthorListSerializer, AuthorDetailsSerializer
from author.models import Author


class AuthorListView(APIView):
    permission_classes = [IsAdmin]
    throttle_classes = [CustomRateThrottle]

    @handle_exceptions
    def get(self, request, pk=None, details=None):
        try:
            if pk:
                author = get_model_by_pk("author", "Author", pk)
                serializer = self.serializer_class(author)
                return Response(serializer.data)
            if details:
                authors = Author.list_with_books(request)
                return paginate_queryset(
                    request,
                    authors,
                    AuthorDetailsSerializer,
                    context={"action": "list_with_books", "request": request},
                )

            else:
                authors = Author.list(request)
                return paginate_queryset(request, authors, AuthorListSerializer)
        except Exception as e:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=AuthorListSerializer.errors,
            )


class AuthorCreateView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = AuthorListSerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": _("Author is successfully created")},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)


class AuthorUpdateView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = AuthorListSerializer

    @handle_exceptions
    def patch(self, request, pk):
        author = get_model_by_pk("author", "Author", pk)

        serializer = self.serializer_class(
            instance=author, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Author updated successfully")}, status=200)
        raise CustomException(status_code=400, errors=serializer.errors)


class AuthorDeleteView(APIView):
    permission_classes = [IsAdmin]

    @handle_exceptions
    def delete(self, request, pk):
        author = get_model_by_pk("author", "Author", pk)
        author.delete()
        return Response(data={"message": _("Author deleted successfully")})
