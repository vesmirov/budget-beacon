from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Profile, User


class ExtendedUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {'fields': ('telegram_id', 'role')},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None, {'fields': ('telegram_id', 'role')},
        ),
    )

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'telegram_id',
        'is_staff',
        'is_active',
        'date_joined',
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telegram_id')
    list_filter = ('is_staff', 'is_active', 'date_joined')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'budget', 'budget_period', 'currency', 'date_updated',)


admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Profile, ProfileAdmin)
