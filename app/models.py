from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'is_staff must be True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'is_superuser must be true')
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('Email ID is required for creating the user'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(_('Email Address'), unique=True)
    otp = models.IntegerField(_('OTP'), null=True, blank=True)
    pattern_order = models.CharField(
        _('Sequence'), max_length=3)
    temp_blocked = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.email)
