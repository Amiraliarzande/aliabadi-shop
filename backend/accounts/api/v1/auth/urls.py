from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterView.as_view(),
        name="token-refresh",
    ),
    path(
        "verify/",
        views.VerifyView.as_view(),
        name="verify",
    ),
    path(
        "verify/resend/",
        views.ResendOTPView.as_view(),
        name="verify-resend",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "password-reset/request/",
        views.PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),

    path(
        "password-reset/verify/",
        views.PasswordResetVerifyView.as_view(),
        name="password-reset-verify",
    ),

    path(
        "password-reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]