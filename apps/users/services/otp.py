import random
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from users.models import OTPCode


class OTPService:

    @staticmethod
    def generate_code(length=6):
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def can_send_otp(phone):
        key = f"otp_limit_{phone}"
        attempts = cache.get(key, 0)
        return attempts < 5

    @staticmethod
    def mark_attempt(phone):
        key = f"otp_limit_{phone}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, timeout=60)

    @staticmethod
    def send_code(phone):
        if not OTPService.can_send_otp(phone):
            return {"ok": False, "error": "Too many attempts. Try again later."}

        code = OTPService.generate_code()

        OTPCode.objects.create(
            phone=phone,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        OTPService.mark_attempt(phone)

        # TODO: integrate real SMS provider here
        print(f"DEBUG OTP for {phone}: {code}")

        return {"ok": True, "message": "OTP sent."}
