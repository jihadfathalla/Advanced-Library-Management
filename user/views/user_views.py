from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import activate
from utils.exception_handler_decorator import handle_exceptions
from utils.custom_exception_class import CustomException
from permissions.admin_permission_class import IsAdmin


class languageView(APIView):
    permission_classes = [IsAdmin]

    @handle_exceptions
    def post(self, request):
        try:
            lan = request.get(lan)
            activate("lan")
            return Response(
                {"message": "language changed successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            raise CustomException(status_code=400, errors="")
