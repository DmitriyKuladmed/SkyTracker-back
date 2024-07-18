from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from .managers import UserProfileManager


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=False,
        verbose_name="Email пользователя"
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        verbose_name="Username пользователя"
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Является ли user администратором"
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class City(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    city_name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name="Название города"
    )
    search_counter = models.IntegerField(
        null=False,
        default=0,
        verbose_name="Количество раз которое данный город искался",
    )

    last_searched = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего поиска",
    )

    def __str__(self):
        return self.name
