from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.auth_views import (
    UserRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
from .views.user_views import languageView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uid>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "change/language/",
        languageView.as_view(),
        name="change_language",
    ),
]
