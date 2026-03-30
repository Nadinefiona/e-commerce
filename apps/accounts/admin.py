from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Role", {"fields": ("role", "phone", "address")}),)
    list_display = ("id", "username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
