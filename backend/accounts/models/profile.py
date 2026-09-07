from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .user import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def get_full_name(self):
        full_name = (
            f"{self.first_name} "
            f"{self.last_name}"
        ).strip()

        return full_name or "کاربر جدید"

    def __str__(self):
        return self.get_full_name()


@receiver(
    post_save,
    sender=User,
)
def create_profile(
    sender,
    instance,
    created,
    **kwargs,
):
    if created:
        Profile.objects.create(
            user=instance,
        )