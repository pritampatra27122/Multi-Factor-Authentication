from django.contrib import admin
from .models import User


class UserAdminPanel(admin.ModelAdmin):
    fieldsets = (
        (('Personal Info'), {'fields': ('email', 'name', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_superuser')}),
        (('Details'), {'fields': ('otp', 'pattern_order', 'temp_blocked')})
    )

    list_display = ('id', 'email', 'name', 'is_superuser')


admin.site.register(User, UserAdminPanel)
