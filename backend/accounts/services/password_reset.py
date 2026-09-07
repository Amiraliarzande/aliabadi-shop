import hashlib
import secrets
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from accounts.models import PasswordResetToken


class PasswordResetService:

    TOKEN_EXPIRATION_MINUTES = 10

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token):
        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    @classmethod
    @transaction.atomic
    def create_token(cls, user):

        # Invalidate previous unused tokens
        PasswordResetToken.objects.filter(
            user=user,
            is_used=False,
        ).update(
            is_used=True,
        )

        raw_token = cls.generate_token()

        token_hash = cls.hash_token(
            raw_token,
        )

        expires_at = (
            timezone.now()
            + timedelta(
                minutes=cls.TOKEN_EXPIRATION_MINUTES,
            )
        )

        PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        return raw_token

    @classmethod
    def get_valid_token(cls, raw_token):

        token_hash = cls.hash_token(
            raw_token,
        )

        try:
            reset_token = (
                PasswordResetToken.objects
                .select_related("user")
                .get(
                    token_hash=token_hash,
                    is_used=False,
                )
            )
        except PasswordResetToken.DoesNotExist:
            raise ValueError(
                "توکن بازیابی رمز عبور نامعتبر است."
            )

        if reset_token.is_expired():
            raise ValueError(
                "توکن بازیابی رمز عبور منقضی شده است."
            )

        return reset_token

    @classmethod
    @transaction.atomic
    def reset_password(
        cls,
        raw_token,
        password,
    ):

        reset_token = cls.get_valid_token(
            raw_token,
        )

        user = reset_token.user

        user.set_password(password)

        user.save(
            update_fields=[
                "password",
                "updated_at",
            ],
        )

        reset_token.is_used = True

        reset_token.save(
            update_fields=[
                "is_used",
            ],
        )

        return user