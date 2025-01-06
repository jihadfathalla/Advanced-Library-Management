from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.get_model_by_pk import get_model_by_pk
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_paginator import paginate_queryset
from utils.custom_exception_class import CustomException
from permissions.admin_permission_class import IsAdmin


from library.models.library_branch_model import Category
from library.serializers.library_branch_serializer import CategorySerializer


class CategoryListView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer

    @handle_exceptions
    def get(self, request, pk=None):
        try:
            if pk:
                category = get_model_by_pk("library", "Category", pk)
                serializer = self.serializer_class(category)
                return Response(serializer.data)
            else:
                filter_dict = {}

                if request.GET.get("category__name"):
                    filter_dict["books__category__name"] = request.GET.get(
                        "category__name"
                    )
                if request.GET.get("author__name"):
                    filter_dict["books__author__name"] = request.GET.get("author__name")

                Categories = Category.objects.all()
                return paginate_queryset(request, Categories, self.serializer_class)
        except:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=self.serializer_class.errors,
            )


class CategoryCreateView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Category is successfully created"},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)


class CategoryUpdateView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer

    @handle_exceptions
    def patch(self, request, pk):
        category = get_model_by_pk("library", "Category", pk)

        serializer = self.serializer_class(
            instance=category, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category updated successfully"}, status=200)
        raise CustomException(status_code=400, errors=serializer.errors)


class CategoryDeleteView(APIView):
    permission_classes = [IsAdmin]

    @handle_exceptions
    def delete(self, request, pk):
        category = get_model_by_pk("library", "Category", pk)
        category.delete()
        return Response(data={"message": "Category deleted successfully"})
