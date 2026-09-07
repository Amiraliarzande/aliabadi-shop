from django.db import transaction

from rest_framework import serializers

from accounts.models import (
    OTPPurpose,
    Profile,
    User,
    UserType,
)

from accounts.services.otp import OTPService
from accounts.services.password_reset import (
    PasswordResetService,
)


class RegisterSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(
        write_only=True,
        required=True,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User

        fields = [
            "username",
            "phone_number",
            "password",
            "password_confirm",
        ]

    def validate_username(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "نام کاربری نمی‌تواند خالی باشد."
            )

        if User.objects.filter(
            username__iexact=value,
        ).exists():
            raise serializers.ValidationError(
                "این نام کاربری قبلاً استفاده شده است."
            )

        return value

    def validate_phone_number(self, value):

        value = value.strip()

        if Profile.objects.filter(
            phone_number=value,
        ).exists():
            raise serializers.ValidationError(
                "کاربری با این شماره موبایل قبلاً ثبت شده است."
            )

        return value

    def validate(self, attrs):

        if (
            attrs["password"]
            != attrs["password_confirm"]
        ):
            raise serializers.ValidationError(
                {
                    "password_confirm": (
                        "رمز عبور و تکرار آن "
                        "یکسان نیستند."
                    )
                }
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        phone_number = validated_data.pop(
            "phone_number",
        )

        validated_data.pop(
            "password_confirm",
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            type=UserType.CUSTOMER,
        )

        user.profile.phone_number = phone_number

        user.profile.save(
            update_fields=[
                "phone_number",
            ],
        )

        OTPService.create_otp(
            user=user,
            purpose=OTPPurpose.REGISTER,
        )

        return user


class RegisterResponseSerializer(
    serializers.Serializer
):

    user = serializers.SerializerMethodField()

    message = serializers.CharField()

    def get_user(self, obj):

        user = obj["user"]

        return {
            "id": user.id,
            "username": user.username,
            "phone_number": (
                user.profile.phone_number
            ),
            "type": user.type,
            "is_verified": user.is_verified,
        }


class VerifySerializer(serializers.Serializer):

    username = serializers.CharField(
        write_only=True,
    )

    otp = serializers.CharField(
        write_only=True,
        min_length=4,
        max_length=4,
    )

    def validate(self, attrs):

        username = attrs["username"].strip()
        otp_code = attrs["otp"].strip()

        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "username": (
                        "کاربری با این نام کاربری "
                        "وجود ندارد."
                    )
                }
            )

        if user.is_verified:
            raise serializers.ValidationError(
                {
                    "otp": (
                        "این حساب قبلاً تأیید شده است."
                    )
                }
            )

        try:
            user_otp = OTPService.verify_otp(
                user=user,
                code=otp_code,
                purpose=OTPPurpose.REGISTER,
            )
        except ValueError as exc:
            raise serializers.ValidationError(
                {
                    "otp": str(exc),
                }
            )

        attrs["user"] = user
        attrs["user_otp"] = user_otp

        return attrs


class VerifyResponseSerializer(
    serializers.Serializer
):

    user = serializers.SerializerMethodField()

    access = serializers.CharField()

    refresh = serializers.CharField()

    def get_user(self, obj):

        user = obj["user"]

        return {
            "id": user.id,
            "username": user.username,
            "phone_number": (
                user.profile.phone_number
            ),
            "type": user.type,
            "is_verified": user.is_verified,
        }


class ResendOTPSerializer(serializers.Serializer):

    username = serializers.CharField(
        write_only=True,
    )

    def validate_username(self, value):

        value = value.strip()

        try:
            user = User.objects.get(
                username=value,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "کاربری با این نام کاربری وجود ندارد."
            )

        if user.is_verified:
            raise serializers.ValidationError(
                "این حساب قبلاً تأیید شده است."
            )

        self.user = user

        return value


class PasswordResetRequestSerializer(
    serializers.Serializer
):

    username = serializers.CharField(
        write_only=True,
    )

    def validate_username(self, value):

        value = value.strip()

        try:
            user = User.objects.get(
                username=value,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "کاربری با این نام کاربری وجود ندارد."
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                "این حساب هنوز تأیید نشده است."
            )

        self.user = user

        return value

    def save(self, **kwargs):

        OTPService.create_otp(
            user=self.user,
            purpose=OTPPurpose.PASSWORD_RESET,
        )

        return self.user

class PasswordResetVerifySerializer(
    serializers.Serializer
):

    username = serializers.CharField(
        write_only=True,
    )

    otp = serializers.CharField(
        write_only=True,
        min_length=4,
        max_length=4,
    )

    def validate(self, attrs):

        username = attrs["username"].strip()
        otp_code = attrs["otp"].strip()

        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "username": (
                        "کاربری با این نام کاربری "
                        "وجود ندارد."
                    )
                }
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                {
                    "username": (
                        "این حساب هنوز تأیید نشده است."
                    )
                }
            )

        try:
            OTPService.verify_otp(
                user=user,
                code=otp_code,
                purpose=OTPPurpose.PASSWORD_RESET,
            )
        except ValueError as exc:
            raise serializers.ValidationError(
                {
                    "otp": str(exc),
                }
            )

        reset_token = (
            PasswordResetService.create_token(
                user=user,
            )
        )

        attrs["user"] = user
        attrs["reset_token"] = reset_token

        return attrs

class PasswordResetConfirmSerializer(
    serializers.Serializer
):

    reset_token = serializers.CharField(
        write_only=True,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        if (
            attrs["password"]
            != attrs["password_confirm"]
        ):
            raise serializers.ValidationError(
                {
                    "password_confirm": (
                        "رمز عبور و تکرار آن "
                        "یکسان نیستند."
                    )
                }
            )

        return attrs

    def save(self, **kwargs):

        user = PasswordResetService.reset_password(
            raw_token=self.validated_data[
                "reset_token"
            ],
            password=self.validated_data[
                "password"
            ],
        )

        return user