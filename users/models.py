from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='номер телефона', null=True, blank=True)
    telegram = models.CharField(max_length=150, verbose_name='Telegram username', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []