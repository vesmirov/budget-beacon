from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """Represents a currency that the user can use."""

    name = models.CharField(_('name'), max_length=32, unique=True)
    iso_code = models.CharField(_('ISO code'), max_length=3, unique=True)


class Fund(models.Model):
    """Reflects a fund or budget category that a user can create."""

    name = models.CharField(_('name'), max_length=32)
    description = models.CharField(_('description'), max_length=200, null=True)
    balance = models.DecimalField(_('balance'), decimal_places=2)
    goal = models.DecimalField(_('goal'), decimal_places=2, null=True)
    budget = models.DecimalField(_('balance'), decimal_places=2)
    date = models.DateTimeField(_('date created'), auto_now_add=True)


class Transaction(models.Model):
    """Represents a record of each transaction of the user."""

    class TransactionTypeChoices(models.TextChoices):
        INCOME = 'IN', _('Income')
        EXPENSE = 'EX', _('Expense')
        TRANSFER = 'TR', _('Transfer')

    amount = models.DecimalField(_('transferred amount'), decimal_places=2)
    comment = models.CharField(_('comment'), max_length=200, null=True)
    date = models.DateTimeField(_('date'), auto_now_add=True)
