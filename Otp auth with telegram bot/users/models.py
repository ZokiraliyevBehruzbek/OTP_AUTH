from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.BigIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class OTP(models.Model):
    session_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    telegram_id = models.BigIntegerField()   
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)