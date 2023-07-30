from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from finances.models import Currency


class User(AbstractUser):
    """
    This User model extends Django's AbstractUser model to add extra fields that you need for your application.
    Specifically, it includes a field for the user's Telegram ID, which allows your application to interact with
    the user through the Telegram messaging service.
    """

    telegram_id = models.CharField(_('telegram ID'), max_length=32, unique=True)


class Profile(models.Model):
    """
    The Profile model represents a user's financial profile. It is connected to a User and a Currency model.
    It includes the user's current balance and preferred currency, as well as the user's preferred budgeting
    period (daily, weekly, monthly, or annually).
    """

    class PeriodChoices(models.TextChoices):
        DAILY = 'D', _('Daily')
        WEEKLY = 'W', _('Weekly')
        MONTHLY = 'M', _('Monthly')
        ANNUALLY = 'A', _('Annually')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(_('balance'), decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='profile')
