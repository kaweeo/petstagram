from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from petstagram.accounts.managers import AppUserManager


class AppUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'  # Specifies that the email field will be used as the unique identifier
    REQUIRED_FIELDS = []  # for authentication instead of the default username field.

    objects = AppUserManager()  # User Manager