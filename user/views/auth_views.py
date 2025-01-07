from rest_framework.views import APIView
from rest_framework import status
from django.utils.translation import gettext as _

from rest_framework.response import Response
from ..serializers import (
    UserRegistrationSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("User registered successfully")},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("Password reset link sent to your email.")},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):

    def post(self, request, uid, token):
        serializer = PasswordResetConfirmSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("Password has been reset successfully.")},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
