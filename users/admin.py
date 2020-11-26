from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.


class UserAdminInterface(UserAdmin):
    list_display = ("email", "username", "is_active", "is_superuser", "first_name", "last_name", "phone_number", "birth_date")
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(CustomUser, UserAdminInterface)
