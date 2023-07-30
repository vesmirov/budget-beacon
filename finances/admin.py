from django.contrib import admin

from finances.models import Currency, Fund, Transaction


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'iso_code')
    search_fields = ('id', 'name')
    ordering = ('name',)


class FundAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user_profile',
        'date_created',
        'date_updated',
    )
    search_fields = ('id', 'name', 'description')
    list_filter = ('date_created', 'date_updated', 'user_profile__id')
    ordering = ('id', 'user_profile__id')
    list_per_page = 50
    list_select_related = True


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'fund',
        'date_created',
        'user_profile',
        'comment',
    )
    search_fields = ('id', 'comment',)
    list_filter = ('date_created', 'user_profile__id', 'fund__id')
    list_per_page = 50
    list_select_related = True


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(Transaction, TransactionAdmin)
