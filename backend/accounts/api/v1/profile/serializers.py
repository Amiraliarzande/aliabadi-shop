from rest_framework import serializers

from accounts.models import Profile


class ProfileRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "image",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "image",
        ]

    def validate_phone_number(self, value):

        value = value.strip()

        if value and (
            not value.isdigit()
            or len(value) != 11
        ):
            raise serializers.ValidationError(
                "شماره موبایل باید ۱۱ رقم باشد."
            )

        queryset = Profile.objects.filter(
            phone_number=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if value and queryset.exists():
            raise serializers.ValidationError(
                "این شماره موبایل قبلاً استفاده شده است."
            )

        return value


class ProfilePartialUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Profile

        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "image",
        ]

    def validate_phone_number(self, value):

        value = value.strip()

        if value and (
            not value.isdigit()
            or len(value) != 11
        ):
            raise serializers.ValidationError(
                "شماره موبایل باید ۱۱ رقم باشد."
            )

        queryset = Profile.objects.filter(
            phone_number=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if value and queryset.exists():
            raise serializers.ValidationError(
                "این شماره موبایل قبلاً استفاده شده است."
            )

        return value


class ProfileDeleteSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Profile

        fields = [
            "id",
        ]

        read_only_fields = [
            "id",
        ]