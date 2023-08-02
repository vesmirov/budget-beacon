from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    This User model extends Django's AbstractUser model to add extra fields that you need for your application.
    Specifically, it includes a field for the user's Telegram ID, which allows your application to interact with
    the user through the Telegram messaging service.

    The user has several roles:
    1. ADMIN - administrator
    2. UNREGISTERED - regular user, who was created and can be managed by admin only
    3. REGISTERED - regular user, who was created, confirmed and can be managed by both admin and himself

    Fields:
        role (str): choice filed which represents the type of created user
        telegram_id (str): telegram user ID
        password (str): optional, if user is UNREGISTERED, otherwise is mandatory
    """

    class UserRolesChoices(models.TextChoices):
        ADMIN = 'ADM', _('Admin User')
        UNREGISTERED = 'UNR', _('Unregistered User')
        REGISTERED = 'REG', _('Registered User')

    role = models.CharField(_('role'), max_length=3, choices=UserRolesChoices.choices)
    telegram_id = models.CharField(_('telegram ID'), max_length=32, unique=True)
    password = models.CharField(_('password'), max_length=128, blank=True)

    def clean(self):
        if self.role == self.UserRolesChoices.REGISTERED and not (self.password or self.email):
            raise ValidationError(_('Registered users must have an email and password.'))


class Profile(models.Model):
    """
    The Profile model represents a user's financial profile. It is connected to a User and a Currency model.
    It includes the user's current balance and preferred currency, as well as the user's preferred budgeting
    period (daily, weekly, monthly, or annually).

    Fields:
        user (oo): 'User' OneToOne relation
        balance (dec): the amount of non-distributed money
        currency (fk): `Currency` OneToMany relation
        date_created (dt): date and time profile was created
        date_updated (dt): date and time profile was updated
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(_('balance'), decimal_places=2, max_digits=15)
    currency = models.ForeignKey('finances.Currency', on_delete=models.PROTECT, related_name='user_profiles', null=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
