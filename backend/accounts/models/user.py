from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserType(models.IntegerChoices):
    CUSTOMER = 1, _("customer")
    ADMIN = 2, _("admin")
    SUPERUSER = 3, _("superuser")


class UserManager(BaseUserManager):

    def create_user(
        self,
        username,
        password=None,
        **extra_fields,
    ):
        if not username:
            raise ValueError(_("Username must be set"))

        username = username.strip()

        user = self.model(
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username,
        password,
        **extra_fields,
    ):
        extra_fields.setdefault(
            "is_staff",
            True,
        )

        extra_fields.setdefault(
            "is_superuser",
            True,
        )

        extra_fields.setdefault(
            "is_active",
            True,
        )

        extra_fields.setdefault(
            "is_verified",
            True,
        )

        extra_fields.setdefault(
            "type",
            UserType.SUPERUSER,
        )

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must have is_staff=True.")
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must have is_superuser=True.")
            )

        return self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    type = models.IntegerField(
        choices=UserType.choices,
        default=UserType.CUSTOMER,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class OTPPurpose(models.TextChoices):
    REGISTER = "register", _("Register")
    PASSWORD_RESET = "password_reset", _("Password reset")

class UserOTP(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    otp_code = models.CharField(
        max_length=6,
    )

    purpose = models.CharField(
        max_length=30,
        choices=OTPPurpose.choices,
        default="register",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_used = models.BooleanField(
        default=False,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "user",
                    "purpose",
                    "otp_code",
                ],
            ),
        ]

    def is_expired(self, minutes=5):
        return timezone.now() > (
            self.created_at + timedelta(
                minutes=minutes,
            )
        )

    def mark_used(self):
        self.is_used = True

        self.save(
            update_fields=[
                "is_used",
            ],
        )


class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )

    token_hash = models.CharField(
        max_length=128,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False,
    )

    def is_expired(self):
        return timezone.now() >= self.expires_at