from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.get_model_by_pk import get_model_by_pk
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_paginator import paginate_queryset
from utils.custom_exception_class import CustomException
from permissions.admin_or_librarian_permission_class import IsAdminOrLibrarian

from library.models.library_model import Library
from library.models.library_branch_model import LibraryBranch
from library.serializers.library_serializer import LibrarySerializer

from user.models import User


class LibraryListView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = LibrarySerializer

    @handle_exceptions
    def get(self, request, pk=None):
        try:
            if pk:
                library = get_model_by_pk("library", "Library", pk)
                serializer = self.serializer_class(library)
                return Response(serializer.data)
            else:
                libraries = Library.list(request)
                return paginate_queryset(request, libraries, self.serializer_class)
        except:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=self.serializer_class.errors,
            )


class LibraryCreateView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = LibrarySerializer

    @handle_exceptions
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Library is successfully created"},
                status=status.HTTP_201_CREATED,
            )
        raise CustomException(status_code=400, errors=serializer.errors)


class LibraryUpdateView(APIView):
    permission_classes = [IsAdminOrLibrarian]
    serializer_class = LibrarySerializer

    @handle_exceptions
    def patch(self, request, pk):
        library = get_model_by_pk("library", "Library", pk)

        serializer = self.serializer_class(
            instance=library, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Library updated successfully"}, status=200)
        raise CustomException(status_code=400, errors=serializer.errors)


class LibraryDeleteView(APIView):
    permission_classes = [IsAdminOrLibrarian]

    @handle_exceptions
    def delete(self, request, pk):
        library = get_model_by_pk("library", "Library", pk)
        library.delete()
        return Response(data={"message": "Library deleted successfully"})


class NearbyLibraryView(APIView):
    permission_classes = [IsAdminOrLibrarian]

    @handle_exceptions
    def get(self, request):
        try:
            users = User.objects.all()
            branches = LibraryBranch.objects.all()
            results = []
            for user in users:
                nearby_branches = []
                for branch in branches:
                    distance = user.get_nearby_libraries(branch)
                    nearby_branches.append(
                        {
                            "branch_name": branch.branch_name,
                            "library_name": branch.library.name,
                            "distance": distance,
                        }
                    )

                nearby_branches.sort(key=lambda x: x["distance"])
                results.append(
                    {"user": user.id, "nearby_libraries": nearby_branches[:5]}
                )
            return Response({"data": results}, status=200)
        except Exception as e:
            return Response(
                {"message": f"something wrong, error is {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
