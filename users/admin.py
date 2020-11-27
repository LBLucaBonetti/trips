from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Conferma della password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        exclude = ("is_staff", "is_admin")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password non coincidenti")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        exclude = ("is_staff", "is_admin")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "username", "is_active", "is_superuser", "first_name", "last_name", "phone_number", "birth_date")
    list_filter = ("is_superuser",)
    fieldsets = (
        ("Informazioni", {"fields": ("email", "username", "is_active")}),
        ("Permessi", {"fields": ("is_superuser",)}),
        ("Dati personali", {"fields": ("first_name", "last_name", "phone_number", "birth_date")}),
        ("Credenziali", {"fields": ("password",)})
    )
    add_fieldsets = (
        ("Informazioni", {
            "classes": ("wide",),
            "fields": ("email", "username", "is_active"),
        }),
        ("Permessi", {
            "classes": ("wide",),
            "fields": ("is_superuser",),
        }),
        ("Dati personali", {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "phone_number", "birth_date"),
        }),
        ("Credenziali", {
            "classes": ("wide",),
            "fields": ("password1", "password2"),
        })
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
