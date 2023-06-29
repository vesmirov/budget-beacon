from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    password = models.CharField('password hash', max_length=128)
    telegram_id = models.CharField('telegram ID', max_length=32)
