from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
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

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


