from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Profile

User = get_user_model()


class Currency(models.Model):
    """
    Represents a currency that the user can use.

    Fields:
        name (str): currency name
        iso_code (str): currency ISO code
    """

    name = models.CharField(_('name'), max_length=32, unique=True)
    iso_code = models.CharField(_('ISO code'), max_length=3, unique=True)


class Fund(models.Model):
    """
    Reflects a fund or budget category that a user can create.

    Fields:
        name (str): fund name
        description (str): fund description (optional)
        balance (dec): fund current balance
        goal (dec): fund goal balance (optional)
        budget (dec): planned fund budget for `self.user.profile.budget_period`
        date (dt): date and time budget was created
        user (fk): `User` OneToMany relation
    """

    name = models.CharField(_('name'), max_length=32)
    description = models.CharField(_('description'), max_length=200, blank=True)
    balance = models.DecimalField(_('balance'), decimal_places=2, max_digits=15)
    goal = models.DecimalField(_('goal'), decimal_places=2, max_digits=15, blank=True)
    budget = models.DecimalField(_('balance'), decimal_places=2, max_digits=15)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='funds')


class Transaction(models.Model):
    """
    Represents a record of each transaction of the user.

    Each transaction involves an amount of money being transferred, and can be classified as
    either an income, an expense, or a transfer. The transaction is linked to a fund and
    the user's profile. It can optionally include a comment for additional details.

    Fields:
        amount (dec): the amount of money involved in the transaction
        comment (str): a comment providing more details about the transaction (optional)
        date_created (dt): the date and time when the transaction was recorded
        fund (fk): `Fund` OneToMany relation
        user_profile (fk): `Profile` OneToMany relation
    """

    class TransactionTypeChoices(models.TextChoices):
        INCOME = 'IN', _('Income')
        EXPENSE = 'EX', _('Expense')
        TRANSFER = 'TR', _('Transfer')

    type = models.CharField(_('transaction type'), max_length=2, choices=TransactionTypeChoices.choices)
    amount = models.DecimalField(_('transferred amount'), decimal_places=2, max_digits=15)
    comment = models.CharField(_('comment'), max_length=200, blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='transactions')
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transactions')
