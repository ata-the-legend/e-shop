from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), max_length=254, unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=11, unique=True)
    full_name = models.CharField(_("Full Name"), max_length=100)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_admin = models.BooleanField(_("Is Admin"), default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


    @property
    def is_staff(self):
        return self.is_admin



class OtpCode(models.Model):
    phone_number = models.CharField(_("phone number"), max_length=11)
    code = models.PositiveSmallIntegerField(_("code"))
    created = models.DateTimeField(_("Created at"), auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return f'{self.phone_number} - {self.code} - {self.created}'
