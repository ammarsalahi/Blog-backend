from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .manager import UserManager


# def get_default_image():
#     return 'users/photo/userimg.png'

class User(AbstractBaseUser):
    full_name = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=200,
        unique=True
    )
    email = models.EmailField(
        unique=True
    )

    is_superuser = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=False
    )
    is_two_factor_auth =models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username
