from django.db import transaction

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import OTPPurpose
from accounts.services.otp import OTPService

from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    RegisterResponseSerializer,
    RegisterSerializer,
    ResendOTPSerializer,
    VerifyResponseSerializer,
    VerifySerializer,
)


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):

        self.user = serializer.save()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_create(
            serializer,
        )

        response_data = {
            "user": self.user,
            "message": (
                "کد تأیید به شماره موبایل "
                "شما ارسال شد."
            ),
        }

        return Response(
            RegisterResponseSerializer(
                response_data,
            ).data,
            status=201,
        )


class VerifyView(generics.CreateAPIView):

    serializer_class = VerifySerializer

    permission_classes = [
        AllowAny,
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data[
            "user"
        ]

        user.is_verified = True

        user.save(
            update_fields=[
                "is_verified",
            ],
        )

        refresh = RefreshToken.for_user(
            user,
        )

        response_data = {
            "user": user,
            "access": str(
                refresh.access_token,
            ),
            "refresh": str(
                refresh,
            ),
        }

        return Response(
            VerifyResponseSerializer(
                response_data,
            ).data,
            status=200,
        )


class ResendOTPView(generics.CreateAPIView):

    serializer_class = ResendOTPSerializer

    permission_classes = [
        AllowAny,
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.user

        OTPService.create_otp(
            user=user,
            purpose=OTPPurpose.REGISTER,
        )

        return Response(
            {
                "message": (
                    "کد تأیید جدید "
                    "ارسال شد."
                ),
            },
            status=200,
        )


class PasswordResetRequestView(
    generics.CreateAPIView
):

    serializer_class = PasswordResetRequestSerializer

    permission_classes = [
        AllowAny,
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            {
                "message": (
                    "کد بازیابی رمز عبور "
                    "ارسال شد."
                ),
            },
            status=200,
        )


class PasswordResetVerifyView(
    generics.CreateAPIView
):

    serializer_class = PasswordResetVerifySerializer

    permission_classes = [
        AllowAny,
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            {
                "reset_token": (
                    serializer.validated_data[
                        "reset_token"
                    ]
                ),
                "message": (
                    "کد تأیید شد."
                ),
            },
            status=200,
        )


class PasswordResetConfirmView(
    generics.CreateAPIView
):

    serializer_class = PasswordResetConfirmSerializer

    permission_classes = [
        AllowAny,
    ]

    @transaction.atomic
    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            {
                "message": (
                    "رمز عبور با موفقیت "
                    "تغییر کرد."
                ),
            },
            status=200,
        )