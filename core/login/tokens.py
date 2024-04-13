import random
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils import timezone
import datetime
from .models import *

class TokenGenerator:
    """
    Custom token generator to create a 6-digit OTP.
    """

    def _make_token_for_user(self, user):
        """
        Generates a 6-digit OTP for the given user.
        """
        token = str(random.randint(100000, 999999))
        profile, created = Profile.objects.get_or_create(user=user)
        profile.otp_token = token
        profile.otp_token_expiry = timezone.now() + datetime.timedelta(minutes=10)  # Token is valid for 10 minutes
        profile.save()
        return token

    def send_verification_email(self, user):
        """
        Sends a verification email with an OTP to the user.
        """
        token = self._make_token_for_user(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        message = f"Your verification code is: {token}"
        send_mail(
            "Verify Your Email for registration",
            message,
            "your_email@example.com",
            [user.email],
            fail_silently=False,
        )

    def verify_token(self, user, token):
        """
        Verifies the OTP for the given user.
        """
        try:
            profile = user.profile
            if profile.otp_token == token and profile.otp_token_expiry > timezone.now():
                return True
        except Profile.DoesNotExist:
            pass
        return False