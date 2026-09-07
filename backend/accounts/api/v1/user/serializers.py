from rest_framework import serializers

from accounts.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "created_at",
            "updated_at",
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "created_at",
            "updated_at",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "username",
        ]

    def validate_username(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "نام کاربری نمی‌تواند خالی باشد."
            )

        queryset = User.objects.filter(
            username__iexact=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "این نام کاربری قبلاً استفاده شده است."
            )

        return value


class UserDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
        ]

        read_only_fields = [
            "id",
        ]