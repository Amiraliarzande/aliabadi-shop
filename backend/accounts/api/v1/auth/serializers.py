from django.db import transaction

from rest_framework import serializers

from accounts.models import (
    Profile,
    User,
    UserType,
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

        return user


class RegisterResponseSerializer(
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