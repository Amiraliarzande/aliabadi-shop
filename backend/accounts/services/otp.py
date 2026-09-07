import secrets

from django.db import transaction

from accounts.models import OTPPurpose, UserOTP


class OTPService:

    @staticmethod
    def generate_code():
        return f"{secrets.randbelow(10000):04d}"

    @classmethod
    @transaction.atomic
    def create_otp(cls, user, purpose):

        UserOTP.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        ).update(
            is_used=True,
        )

        code = cls.generate_code()

        otp = UserOTP.objects.create(
            user=user,
            otp_code=code,
            purpose=purpose,
        )

        print(
            f"[OTP] "
            f"user={user.username} "
            f"purpose={purpose} "
            f"phone={user.profile.phone_number} "
            f"code={code}"
        )

        return otp

    @classmethod
    def verify_otp(
        cls,
        user,
        code,
        purpose,
    ):
        try:
            user_otp = (
                user.otps
                .filter(
                    otp_code=code,
                    purpose=purpose,
                    is_used=False,
                )
                .latest("created_at")
            )
        except UserOTP.DoesNotExist:
            raise ValueError(
                "کد تأیید نامعتبر است."
            )

        if user_otp.is_expired():
            raise ValueError(
                "کد تأیید منقضی شده است."
            )

        user_otp.mark_used()

        return user_otp