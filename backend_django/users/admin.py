from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'first_name', 'last_name', 'role']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email']
    exclude = ['password']
    filter_horizontal = [
        'groups',
        'user_permissions',
    ]
    save_on_top = True
    fieldsets = (
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'role',
                    'image',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )